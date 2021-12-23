<template>
  <CCard class="mb-4">
    <CCardBody>
      <CusTable />
    </CCardBody>
  </CCard>
</template>
<script>
import CusTable from '../Customers//CusTable.vue'

export default {
  name: 'CustomerList',
  components: {
    CusTable,
  },
}
</script>
