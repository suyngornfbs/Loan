<template>
  <CCard class="mb-4">
    <CCardBody>
      <DisTable />
    </CCardBody>
  </CCard>
</template>
<script>
import DisTable from '../Disbursements/DisTable.vue'

export default {
  name: 'Disbursed',
  components: {
    DisTable,
  },
}
</script>
