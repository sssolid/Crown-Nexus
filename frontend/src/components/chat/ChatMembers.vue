<!-- frontend/src/components/chat/ChatMembers.vue -->
<template>
  <div class="chat-members">
    <div class="panel-header">
      <h3>Members ({{ members.length }})</h3>
      <v-btn icon variant="text" @click="$emit('close')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </div>

    <div class="search-container">
      <v-text-field
        v-model="searchQuery"
        placeholder="Search members"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        density="compact"
        hide-details
        class="search-field"
      ></v-text-field>
    </div>

    <div class="member-actions">
      <v-btn
        v-if="canManageMembers"
        block
        color="primary"
        prepend-icon="mdi-account-plus"
        @click="$emit('add-member')"
        class="mb-4"
      >
        Add Member
      </v-btn>
    </div>

    <div class="members-list">
      <v-list>
        <!-- Online members -->
        <v-list-subheader v-if="onlineMembers.length > 0">
          Online — {{ onlineMembers.length }}
        </v-list-subheader>

        <v-list-item
          v-for="member in onlineMembers"
          :key="member.user_id"
          :title="member.user_name"
          :subtitle="getMemberRoleDisplay(member.role)"
        >
          <template v-slot:prepend>
            <v-avatar color="primary" size="36">
              <span>{{ getMemberInitials(member.user_name) }}</span>
            </v-avatar>
            <v-icon color="success" size="12" class="status-icon">mdi-circle</v-icon>
          </template>

          <template v-slot:append>
            <member-actions-menu
              v-if="canManageUser(member)"
              :member="member"
              :is-current-user="isCurrentUser(member)"
              @update-role="updateMemberRole"
              @remove-member="removeMember"
            />
          </template>
        </v-list-item>

        <!-- Offline members -->
        <v-list-subheader v-if="offlineMembers.length > 0">
          Offline — {{ offlineMembers.length }}
        </v-list-subheader>

        <v-list-item
          v-for="member in offlineMembers"
          :key="member.user_id"
          :title="member.user_name"
          :subtitle="getMemberRoleDisplay(member.role)"
        >
          <template v-slot:prepend>
            <v-avatar color="grey-lighten-2" size="36">
              <span>{{ getMemberInitials(member.user_name) }}</span>
            </v-avatar>
          </template>

          <template v-slot:append>
            <member-actions-menu
              v-if="canManageUser(member)"
              :member="member"
              :is-current-user="isCurrentUser(member)"
              @update-role="updateMemberRole"
              @remove-member="removeMember"
            />
          </template>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ChatMember, ChatRoom, ChatMemberRole } from '@/types/chat';

// Member Actions Menu Component (inline)
const MemberActionsMenu = defineComponent({
  name: 'MemberActionsMenu',
  props: {
    member: {
      type: Object as PropType<ChatMember>,
      required: true
    },
    isCurrentUser: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update-role', 'remove-member'],
  setup(props, { emit }) {
    const showMenu = ref(false);

    return {
      showMenu,
      updateRole(role: string) {
        emit('update-role', props.member.user_id, role);
      },
      removeMember() {
        emit('remove-member', props.member);
      }
    };
  },
  template: `
    <v-menu v-model="showMenu" location="bottom end">
      <template v-slot:activator="{ props }">
        <v-btn icon size="small" variant="text" v-bind="props">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-list density="compact">
        <v-list-item
          v-if="!isCurrentUser"
          prepend-icon="mdi-shield-account"
          title="Make Admin"
          @click="updateRole('admin')"
          v-show="member.role !== 'admin' && member.role !== 'owner'"
        ></v-list-item>

        <v-list-item
          v-if="!isCurrentUser"
          prepend-icon="mdi-account"
          title="Make Member"
          @click="updateRole('member')"
          v-show="member.role === 'admin'"
        ></v-list-item>

        <v-list-item
          v-if="!isCurrentUser"
          prepend-icon="mdi-account-remove"
          title="Remove from Room"
          @click="removeMember"
          class="text-error"
          v-show="member.role !== 'owner'"
        ></v-list-item>

        <v-list-item
          v-if="isCurrentUser"
          prepend-icon="mdi-exit-to-app"
          title="Leave Room"
          @click="removeMember"
          class="text-error"
          v-show="member.role !== 'owner'"
        ></v-list-item>
      </v-list>
    </v-menu>
  `
});

const props = defineProps<{
  members: ChatMember[];
  room: ChatRoom;
  currentUserId: string;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'add-member'): void;
  (e: 'remove-member', member: ChatMember): void;
  (e: 'update-role', userId: string, role: string): void;
}>();

// State
const searchQuery = ref('');

// Computed properties
const filteredMembers = computed(() => {
  if (!searchQuery.value.trim()) {
    return props.members;
  }

  const query = searchQuery.value.toLowerCase();
  return props.members.filter(member =>
    member.user_name.toLowerCase().includes(query)
  );
});

const onlineMembers = computed(() => {
  return filteredMembers.value.filter(member => member.is_online);
});

const offlineMembers = computed(() => {
  return filteredMembers.value.filter(member => !member.is_online);
});

const currentUserRole = computed(() => {
  const currentUser = props.members.find(member => member.user_id === props.currentUserId);
  return currentUser ? currentUser.role : null;
});

const canManageMembers = computed(() => {
  return currentUserRole.value === ChatMemberRole.ADMIN ||
    currentUserRole.value === ChatMemberRole.OWNER;
});

// Methods
function getMemberInitials(name: string): string {
  if (!name) return '';

  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

function getMemberRoleDisplay(role: string): string {
  switch (role) {
    case ChatMemberRole.OWNER:
      return 'Owner';
    case ChatMemberRole.ADMIN:
      return 'Admin';
    case ChatMemberRole.MEMBER:
      return 'Member';
    default:
      return role;
  }
}

function isCurrentUser(member: ChatMember): boolean {
  return member.user_id === props.currentUserId;
}

function canManageUser(member: ChatMember): boolean {
  // Can't manage users with higher roles
  if (member.role === ChatMemberRole.OWNER) {
    return false;
  }

  // Admins can't manage other admins
  if (member.role === ChatMemberRole.ADMIN && currentUserRole.value === ChatMemberRole.ADMIN) {
    return false;
  }

  // User can manage themselves (to leave)
  if (isCurrentUser(member)) {
    return true;
  }

  // Otherwise, only admins and owners can manage
  return canManageMembers.value;
}

function updateMemberRole(userId: string, role: string) {
  emit('update-role', userId, role);
}

function removeMember(member: ChatMember) {
  emit('remove-member', member);
}
</script>

<style scoped>
.chat-members {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--v-neutral-200);
}

.panel-header h3 {
  margin: 0;
}

.search-container {
  padding: 16px 16px 8px;
}

.search-field {
  margin-bottom: 8px;
}

.member-actions {
  padding: 0 16px;
}

.members-list {
  flex-grow: 1;
  overflow-y: auto;
}

.status-icon {
  position: absolute;
  bottom: 12px;
  left: 32px;
  border: 2px solid var(--v-surface-base);
  border-radius: 50%;
}
</style>
