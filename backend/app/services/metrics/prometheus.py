# backend/app/services/metrics/prometheus.py
"""Prometheus integration for metrics.

This module provides integration with Prometheus for exposing metrics,
including HTTP server setup and push gateway support.
"""
from __future__ import annotations

import asyncio
import time
from typing import Optional

from prometheus_client import REGISTRY, start_http_server, push_to_gateway

from app.core.logging import get_logger
from app.services.metrics.base import MetricsConfig

logger = get_logger(__name__)


class PrometheusManager:
    """Manager for Prometheus integration."""

    def __init__(self, config: MetricsConfig):
        """
        Initialize the Prometheus manager.

        Args:
            config: Metrics configuration
        """
        self.config = config
        self.initialized = False
        self.server_started = False
        self.push_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """
        Initialize Prometheus integration.

        This sets up the HTTP metrics endpoint and/or push gateway
        based on configuration.
        """
        if self.initialized:
            return

        # Start HTTP server if enabled
        if self.config.enable_prometheus and self.config.enable_endpoint:
            self._start_http_server()

        # Start metrics pushing if configured
        if self.config.enable_prometheus and self.config.push_gateway:
            self.push_task = asyncio.create_task(self._start_push_loop())

        self.initialized = True
        logger.info("Prometheus integration initialized")

    def _start_http_server(self) -> None:
        """Start Prometheus HTTP server."""
        if self.server_started:
            return

        try:
            start_http_server(self.config.endpoint_port)
            self.server_started = True
            logger.info(f"Prometheus metrics endpoint started on port {self.config.endpoint_port}")
        except Exception as e:
            logger.error(f"Failed to start Prometheus HTTP server: {str(e)}")

    async def _start_push_loop(self) -> None:
        """Start loop to periodically push metrics to gateway."""
        logger.info(f"Starting metrics push loop (interval: {self.config.push_interval}s)")

        while True:
            try:
                self._push_metrics()
                logger.debug(f"Pushed metrics to gateway: {self.config.push_gateway}")
            except Exception as e:
                logger.error(f"Failed to push metrics to gateway: {str(e)}")

            # Wait for next push interval
            await asyncio.sleep(self.config.push_interval)

    def _push_metrics(self) -> None:
        """Push metrics to Prometheus push gateway."""
        if not self.config.push_gateway:
            return

        try:
            # Lazy import process metrics for performance
            if self.config.enable_process_metrics:
                self._update_process_metrics()

            # Push metrics to gateway
            push_to_gateway(
                self.config.push_gateway,
                job=self.config.namespace,
                registry=REGISTRY
            )
        except Exception as e:
            logger.error(f"Metrics push error: {str(e)}")
            raise

    def _update_process_metrics(self) -> None:
        """Update process metrics like memory usage and CPU time."""
        try:
            import os
            import psutil

            process = psutil.Process(os.getpid())

            # Update metrics directly through the registry or use registry's metrics
            # In a real implementation, you'd call specific process metric collectors

            # Example placeholder:
            # self.process_memory_gauge.set(process.memory_info().rss)
            # self.process_cpu_gauge.set(process.cpu_percent())

            logger.debug("Updated process metrics")
        except ImportError:
            logger.warning("psutil not installed, skipping process metrics update")
        except Exception as e:
            logger.error(f"Error updating process metrics: {str(e)}")

    async def shutdown(self) -> None:
        """Clean up Prometheus resources."""
        # Cancel push task if running
        if self.push_task:
            self.push_task.cancel()
            try:
                await self.push_task
            except asyncio.CancelledError:
                pass

        # Final push to gateway if configured
        if self.config.enable_prometheus and self.config.push_gateway:
            try:
                self._push_metrics()
                logger.info(f"Final metrics push to gateway: {self.config.push_gateway}")
            except Exception as e:
                logger.error(f"Failed to push metrics to gateway: {str(e)}")
