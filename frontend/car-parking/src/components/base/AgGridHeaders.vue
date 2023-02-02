<template>
  <div>
    <div
      v-if="params.enableMenu"
      ref="menuButton"
      class="customHeaderMenuButton"
      @click="onMenuClicked($event)"
    >
      <i class="fa" :class="params.menuIcon"></i>
    </div>
    <div
      v-if="params.enableSorting"
      @click="onSortRequested()"
      class="customHeaderLabel"
    >
      <span class="text-body-2 font-weight-bold">
        {{ params.displayName }}
      </span>
      <v-icon v-show="ascSort" small>mdi-arrow-up</v-icon>
      <v-icon v-show="descSort" small>mdi-arrow-down</v-icon>
    </div>
    <div v-else>
      <span class="text-body-2 font-weight-bold">
        {{ params.displayName }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ascSort: null,
      descSort: null,
      noSort: null,
    };
  },
  beforeMount() {},
  mounted() {
    if (this.params.enableSorting) {
      this.params.column.addEventListener(
        "sortChanged",
        this.onSortChanged.bind(this)
      );
    }
    this.onSortChanged();
  },
  methods: {
    onMenuClicked() {
      this.params.showColumnMenu(this.$refs.menuButton);
    },

    onSortChanged() {
      if (this.params.column.isSortAscending()) {
        this.ascSort = true;
      } else if (this.params.column.isSortDescending()) {
        this.descSort = true;
      } else {
        this.noSort = true;
      }
    },

    onSortRequested() {
      this.ascSort = this.descSort = this.noSort = false;
      if (
        Object.keys(
          this.params.context.listParentComponentContext.sorting
        ).indexOf(this.params.column.colId) == -1
      ) {
        this.ascSort = true;
        this.params.context.listParentComponentContext.sorting[
          this.params.column.colId
        ] = true;
        this.params.context.listParentComponentContext.applyGridSort(
          this.params.column.colId,
          "asc"
        );
      } else if (
        this.params.context.listParentComponentContext.sorting[
          this.params.column.colId
        ]
      ) {
        this.descSort = true;
        this.params.context.listParentComponentContext.sorting[
          this.params.column.colId
        ] = false;
        this.params.context.listParentComponentContext.applyGridSort(
          this.params.column.colId,
          "desc"
        );
      } else if (
        !this.params.context.listParentComponentContext.sorting[
          this.params.column.colId
        ]
      ) {
        this.noSort = true;
        delete this.params.context.listParentComponentContext.sorting[
          this.params.column.colId
        ];
        this.params.context.listParentComponentContext.applyGridSort(
          this.params.column.colId,
          null
        );
      }
    },
  },
};
</script>

<style></style>
