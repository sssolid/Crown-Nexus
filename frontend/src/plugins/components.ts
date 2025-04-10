// src/plugins/components.ts (updated)
import { App } from 'vue'

// Base Components
import BaseButton from '@/components/base/BaseButton.vue'
import BaseTextField from '@/components/base/BaseTextField.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseIcon from '@/components/base/BaseIcon.vue'

// Form Components
import FormTextField from '@/components/form/FormTextField.vue'
import FormSelect from '@/components/form/FormSelect.vue'
import FormBuilder from '@/components/form/FormBuilder.vue'
import FileUpload from '@/components/form/FileUpload.vue'

// Data Components
import DataTable from '@/components/data/DataTable.vue'
import Pagination from '@/components/data/Pagination.vue'

// Common Components
import PageHeader from '@/components/common/PageHeader.vue'
import InfoList from '@/components/common/InfoList.vue'
import DetailCard from '@/components/common/DetailCard.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import SearchFilter from '@/components/common/SearchFilter.vue'

// Dialog Components
import BaseDialog from '@/components/dialogs/BaseDialog.vue'
import FormDialog from '@/components/dialogs/FormDialog.vue'
import ConfirmationDialog from '@/components/dialogs/ConfirmationDialog.vue'

// Notification Components
import NotificationSystem from '@/components/notifications/NotificationSystem.vue'

// Navigation Components
import BaseTabs from '@/components/tabs/BaseTabs.vue'
import BaseAccordion from '@/components/accordion/BaseAccordion.vue'
import Breadcrumbs from '@/components/navigation/Breadcrumbs.vue'

// Tooltip Components
import BaseTooltip from '@/components/tooltips/BaseTooltip.vue'
import BasePopover from '@/components/popovers/BasePopover.vue'

// Chart Components
import BaseChart from '@/components/charts/BaseChart.vue'
import LineChartExample from '@/components/charts/LineChartExample.vue'
import BarChartExample from '@/components/charts/BarChartExample.vue'

// Loading Components
import SkeletonCard from '@/components/loaders/SkeletonCard.vue'
import SkeletonTable from '@/components/loaders/SkeletonTable.vue'
import SkeletonForm from '@/components/loaders/SkeletonForm.vue'

// Display Components
import UserAvatar from '@/components/display/UserAvatar.vue'
import StatusBadge from '@/components/display/StatusBadge.vue'
import EmptyState from '@/components/display/EmptyState.vue'

// Language Components
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

// Map of components to register
const components = {
  // Base Components
  BaseButton,
  BaseTextField,
  BaseCard,
  BaseIcon,

  // Form Components
  FormTextField,
  FormSelect,
  FormBuilder,
  FileUpload,

  // Data Components
  DataTable,
  Pagination,

  // Common Components
  PageHeader,
  InfoList,
  DetailCard,
  ConfirmDialog,
  SearchFilter,

  // Dialog Components
  BaseDialog,
  FormDialog,
  ConfirmationDialog,

  // Notification Components
  NotificationSystem,

  // Navigation Components
  BaseTabs,
  BaseAccordion,
  Breadcrumbs,

  // Tooltip Components
  BaseTooltip,
  BasePopover,

  // Chart Components
  BaseChart,
  LineChartExample,
  BarChartExample,

  // Loading Components
  SkeletonCard,
  SkeletonTable,
  SkeletonForm,

  // Display Components
  UserAvatar,
  StatusBadge,
  EmptyState,

  // Language Components
  LanguageSwitcher,
}

export default {
  install(app: App) {
    // Register all components globally
    Object.entries(components).forEach(([name, component]) => {
      app.component(name, component)
    })
  }
}
