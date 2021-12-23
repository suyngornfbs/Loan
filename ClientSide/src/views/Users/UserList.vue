<template>
  <CCard class="mb-4">
    <CCardBody>
      <UserTable />
    </CCardBody>
  </CCard>
</template>
<script>
import UserTable from '../Users/UserTable.vue'

export default {
  name: 'UserList',
  components: {
    UserTable,
  },
}
</script>
