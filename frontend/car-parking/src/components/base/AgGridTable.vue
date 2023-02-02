<template>
  <div class="pa-4 custom-list">
    <v-row class="ma-0">
      <v-col cols="6" class="text-left" v-if="title">
        <span class="text-h5 text-uppercase font-weight-bold text_color--text">
          {{ title }}
        </span>
      </v-col>
      <v-col
        :cols="title ? '6' : '12'"
        class="d-flex justify-end"
        v-if="hasListActions"
      >
        <slot name="listAction" />
      </v-col>
      <v-col cols="12" v-if="hasAfterTitle">
        <slot name="afterTitle" />
      </v-col>

      <v-col cols="12" v-if="hasFilter">
        <v-row no-gutters class="ma-0">
          <v-col
            cols="12"
            class="py-0 ma-0"
            v-if="filtersOnRight"
            :class="leftFilterSlotClass"
          >
            <slot name="rightFilterSlot" />
          </v-col>
          <v-col cols="3" class="pr-4" :class="filterClass" v-if="searchInput">
            <v-text-field
              label="Search"
              hide-details="auto"
              prepend-inner-icon="mdi-magnify"
              v-model="search"
              outlined
              dense
              clearable
              @keydown.enter="searchTriggered"
              @click:clear="clearSearch"
            ></v-text-field>
            <v-btn
              v-if="searchMagnify"
              small
              fab
              @click="searchTriggered"
              depressed
              color="secondary"
              class="ml-1 mr-2 rounded"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="9" class="py-0 ma-0">
            <v-row no-gutters>
              <v-col cols="3" v-if="isColumnShowVisibility">
                <AgGridColumnSelector
                  :allHeaders="headersForColumnsSelect"
                  :selectedHeaders="headersSelected"
                  :localStorageKey="localStorageKey"
                  itemText="headerName"
                  itemValue="field"
                  @headers-changed="headersChanged"
                />
              </v-col>
              <v-col>
                <slot name="leftFilterSlot" />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12">
        <AgGridVue
          :style="gridStyle"
          class="ag-theme-alpine"
          :columnDefs="isColumnShowVisibility ? headersForTable : tableHeader"
          :default-col-def="defaultColDef"
          :context="{ ...context, ...listParentComponentContext }"
          :grid-options="hasOtherGridOptions ? otherGridOption : gridOptions"
          :suppressDragLeaveHidesColumns="true"
          :rowData="tableData"
          v-on="$listeners"
          @selection-changed="onSelectionChanged"
          @grid-ready="onGridReady"
          :enableBrowserTooltips="true"
        ></AgGridVue>
      </v-col>
      <v-col v-if="total > 0" cols="12" class="d-flex justify-end py-0">
        <Pagination
          :pageNo="pageNo"
          :totalItems="total"
          :pageSize="itemsPerPage"
          @itemsPerPageChange="itemsPerPageChanged"
          @prevPage="prevPage"
          @nextPage="nextPage"
        />
      </v-col>
    </v-row>
    <slot name="dialogs" />
    <slot name="detail" />
  </div>
</template>

<script>
import { AgGridVue } from "ag-grid-vue";
import "ag-grid-community/styles/ag-grid.css"; // Core grid CSS, always needed
import "ag-grid-community/styles/ag-theme-alpine.css"; // Optional theme CSS
import Pagination from "./Pagination.vue";
// import AgGridHeaders from "./AgGridHeaders.vue";
import AgGridColumnSelector from "./AgGridColumnSelector.vue";

export default {
  components: {
    AgGridVue,
    Pagination,
    // agColumnHeader: AgGridHeaders,
    AgGridColumnSelector,
  },
  props: {
    localStorageKey: {
      type: String,
      default: null,
    },
    isColumnShowVisibility: {
      type: Boolean,
      default: false,
    },
    title: {
      required: false,
    },
    total: {
      type: [Number, String],
      default: 0,
    },
    searchInput: {
      type: Boolean,
      default: true,
    },
    searchMagnify: {
      type: Boolean,
      default: false,
    },
    tableData: {
      type: Array,
      required: true,
    },
    tableHeader: {
      type: Array,
      required: true,
    },
    context: {
      type: Object,
      default: () => {},
    },
    hasFilter: {
      type: Boolean,
      default: true,
    },
    filterClass: {
      type: String,
      default: "d-flex",
    },
    leftFilterSlotClass: {
      type: String,
    },
    filtersOnRight: {
      type: Boolean,
      default: false,
    },
    initialCall: {
      type: Boolean,
      default: true,
    },
    parentComponent: {
      type: Object,
      default: () => {},
    },
    otherGridOption: {
      type: Object,
    },
    hasOtherGridOptions: {
      type: Boolean,
      default: false,
    },
    tableScrollable: {
      type: Boolean,
      default: false,
    },
    setInterval: {
      type: Boolean,
      default: false,
    },
    setIntervalDuration: {
      type: Number,
      default: 1000,
    },
    gridStyle: {
      type: Object,
      default() {
        return {
          width: "100%",
          height: "calc(100vh - 380px)",
        };
      },
    },
    hasAfterTitle: {
      type: Boolean,
      default: true,
    },
    hasListActions: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      sorting: {},
      // pagination vars
      itemsPerPage: 10,
      pageNo: 1,
      filters: {},
      gridApi: null,
      headersSelected: [],
      gridColumnApi: null,
      defaultColDef: {
        lockPosition: true,
        flex: 1,
        resizable: true,
        sortable: true,
        autoHeight: true,
        cellStyle: {
          "text-overflow": "ellipsis",
          "white-space": "nowrap",
          overflow: "hidden",
          display: "block",
        },
      },
      gridOptions: {
        onGridSizeChanged: () => {
          if (this.tableScrollable) {
            this.autoSizeAll();
          } else {
            this.gridOptions.api.sizeColumnsToFit();
          }
        },
        tooltipShowDelay: 0,
        suppressRowClickSelection: true,
        suppressDragLeaveHidesColumns: true,
        enableCellTextSelection: true,
      },
      search: null,

      selectedRows: [],

      timeInterval: null,
    };
  },
  watch: {
    search(val) {
      if (val == "") {
        this.clearSearch();
      }
    },
  },
  computed: {
    headersForTable() {
      return [
        ...this.headersSelected,
        this.tableHeader.find(
          (item) => item.field == "actions" || item.field == "warning"
        ),
      ];
    },
    offset() {
      return this.itemsPerPage * (this.pageNo - 1);
    },
    listParentComponentContext() {
      return { listParentComponentContext: this };
    },
    headersForColumnsSelect() {
      return [...this.tableHeader].filter((item) => {
        if (item.field != "actions" && item.field != "warning") {
          return item;
        }
      });
    },
  },
  methods: {
    searchTriggered() {
      if (this.search) {
        this.search = this.search.trim();
        this.itemsPerPageChanged(this.itemsPerPage);
      }
    },
    setQuickFilter(str) {
      this.gridApi.setQuickFilter(str);
    },
    headersChanged(value) {
      this.headersSelected = value;
      localStorage.setItem(this.localStorageKey, JSON.stringify(value));
      // setTimeout(() => {
      //   this.autoSizeAll();
      // }, 100);
      if (this.gridOptions && this.gridOptions.api) {
        this.gridOptions.api.sizeColumnsToFit();
      }
    },
    onSelectionChanged() {
      this.selectedRows = this.gridApi.getSelectedRows();
      this.$emit("selectionChanged", this.selectedRows);
    },
    setSelection(selectedElementIdArray) {
      this.gridApi.forEachNode((node) => {
        node.setSelected(
          selectedElementIdArray.findIndex((item) => item == node.data.id) > -1
        );
      });
    },
    clearSearch() {
      this.search = null;
      this.itemsPerPageChanged(this.itemsPerPage);
    },
    applyGridSort(key, type) {
      if (this.filters && !this.filters.ordering) {
        this.filters.ordering = [];
      }

      if (type == null) {
        delete this.sorting[key];
        this.filters.ordering.splice(
          this.filters.ordering.indexOf(`-${key}`),
          1
        );
      } else if (type == "asc") {
        this.filters.ordering.push(key);
      } else if (type == "desc") {
        this.filters.ordering.splice(
          this.filters.ordering.indexOf(key),
          1,
          `-${key}`
        );
      }
      if (this.filters.ordering.length == 0) {
        delete this.filters.ordering;
      }
      this.itemsPerPageChanged(this.itemsPerPage);
    },
    onGridReady(params) {
      this.gridApi = params.api;
      this.gridColumnApi = params.columnApi;
    },
    itemsPerPageChanged(e) {
      this.pageNo = 1;
      this.itemsPerPage = e;
      if (this.search) {
        this.filters.search = this.search;
      } else {
        delete this.filters.search;
      }

      this.$emit("getList", {
        ...this.filters,
        offset: this.offset,
        limit: this.itemsPerPage,
      });
    },
    prevPage() {
      this.pageNo--;
      this.$emit("getList", {
        ...this.filters,
        offset: this.offset,
        limit: this.itemsPerPage,
      });
    },
    nextPage() {
      this.pageNo++;
      this.$emit("getList", {
        ...this.filters,
        offset: this.offset,
        limit: this.itemsPerPage,
      });
    },
    autoSizeAll() {
      if (!this.hasOtherGridOptions) {
        let allColumnIds = [];
        this.gridOptions.columnApi.getColumns().forEach(function (column) {
          allColumnIds.push(column.colId);
        });
        this.gridOptions.columnApi.autoSizeColumns(allColumnIds);
      } else {
        let allColumnIds = [];
        this.otherGridOption.columnApi.getColumns().forEach(function (column) {
          allColumnIds.push(column.colId);
        });
        this.otherGridOption.columnApi.autoSizeColumns(allColumnIds);
      }
    },
  },
  mounted() {
    if (this.initialCall) {
      this.$emit("getList", {
        ...this.filters,
        offset: this.offset,
        limit: this.itemsPerPage,
      });
    }
    if (this.setInterval) {
      this.timeInterval = setInterval(() => {
        this.$emit("getList", {
          ...this.filters,
          offset: this.offset,
          limit: this.itemsPerPage,
        });
      }, this.setIntervalDuration);
    }
  },
  beforeDestroy() {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  },
};
</script>
