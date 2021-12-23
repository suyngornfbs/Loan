<template>
  <CTable striped hover>
    <CTableHead>
      <CTableRow>
        <CTableHeaderCell scope="col">#</CTableHeaderCell>
        <CTableHeaderCell scope="col">Name</CTableHeaderCell>
        <CTableHeaderCell scope="col">Gender</CTableHeaderCell>
        <CTableHeaderCell scope="col">Phone</CTableHeaderCell>
        <CTableHeaderCell scope="col">Email</CTableHeaderCell>
        <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody>
      <CTableRow>
        <CTableHeaderCell scope="row">1</CTableHeaderCell>
        <CTableDataCell>Mark</CTableDataCell>
        <CTableDataCell>Otto</CTableDataCell>
        <CTableDataCell>@mdo</CTableDataCell>
        <CTableDataCell>@mdo</CTableDataCell>
        <CTableDataCell>
          <div class="m-2">
            <a href="#" class="btn btn-ms btn-success" title="Preview">
              <em class="cis-money"></em> Edit
            </a>
            <a href="#" class="btn btn-ms btn-success" title="Preview">
              <em class="fa fa-eye"></em> Edit
            </a>
            <a href="#" class="btn btn-ms btn-success" title="Preview">
              <em class="fa fa-eye"></em> Edit
            </a>
          </div>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
<script>
export default {
  name: 'Tables',
}
</script>
