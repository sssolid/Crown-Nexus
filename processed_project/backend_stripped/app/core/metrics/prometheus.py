from __future__ import annotations
import asyncio
from typing import Optional
from prometheus_client import REGISTRY, start_http_server, push_to_gateway
from app.logging import get_logger
from app.core.metrics.base import MetricsConfig
logger = get_logger('app.core.metrics.prometheus')
class PrometheusManager:
    def __init__(self, config: MetricsConfig):
        self.config = config
        self.initialized = False
        self.server_started = False
        self.push_task: Optional[asyncio.Task] = None
    async def initialize(self) -> None:
        if self.initialized:
            return
        if self.config.enable_prometheus and self.config.enable_endpoint:
            self._start_http_server()
        if self.config.enable_prometheus and self.config.push_gateway:
            self.push_task = asyncio.create_task(self._start_push_loop())
        self.initialized = True
        logger.info('Prometheus integration initialized')
    def _start_http_server(self) -> None:
        if self.server_started:
            return
        try:
            start_http_server(self.config.endpoint_port)
            self.server_started = True
            logger.info(f'Prometheus metrics endpoint started on port {self.config.endpoint_port}')
        except Exception as e:
            logger.error(f'Failed to start Prometheus HTTP server: {str(e)}')
    async def _start_push_loop(self) -> None:
        logger.info(f'Starting metrics push loop (interval: {self.config.push_interval}s)')
        while True:
            try:
                self._push_metrics()
                logger.debug(f'Pushed metrics to gateway: {self.config.push_gateway}')
            except Exception as e:
                logger.error(f'Failed to push metrics to gateway: {str(e)}')
            await asyncio.sleep(self.config.push_interval)
    def _push_metrics(self) -> None:
        if not self.config.push_gateway:
            return
        try:
            if self.config.enable_process_metrics:
                self._update_process_metrics()
            push_to_gateway(self.config.push_gateway, job=self.config.namespace, registry=REGISTRY)
        except Exception as e:
            logger.error(f'Metrics push error: {str(e)}')
            raise
    def _update_process_metrics(self) -> None:
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            logger.debug('Updated process metrics')
        except ImportError:
            logger.warning('psutil not installed, skipping process metrics update')
        except Exception as e:
            logger.error(f'Error updating process metrics: {str(e)}')
    async def shutdown(self) -> None:
        if self.push_task:
            self.push_task.cancel()
            try:
                await self.push_task
            except asyncio.CancelledError:
                pass
        if self.config.enable_prometheus and self.config.push_gateway:
            try:
                self._push_metrics()
                logger.info(f'Final metrics push to gateway: {self.config.push_gateway}')
            except Exception as e:
                logger.error(f'Failed to push metrics to gateway: {str(e)}')