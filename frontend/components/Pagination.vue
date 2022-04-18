<template>
  <div v-if="maxPage > 1" class="pagination">
    <button
      :class="{
        'pagination__page': true,
        'pagination__page--disabled': _page <= 1,
      }"
      @click="() => _page > 1 ? goto(_page - 1) : null"
    >
      &larr;
    </button>
    <button v-if="from > 0" class="pagination__page" @click="() => goto(1)">1</button>
    <button v-if="from > 1" class="pagination__page pagination__page--inactive">...</button>
    <button
      v-for="num in to - from"
      :key="num"
      :class="{
        'pagination__page': true,
        'pagination__page--selected': from + num === _page,
        'pagination__page--inactive': from + num === _page,
      }"
      @click="() => goto(from + num)"
    >
      {{ from + num }}
    </button>
    <button v-if="to < maxPage - 1" class="pagination__page pagination__page--inactive">...</button>
    <button v-if="to < maxPage" class="pagination__page" @click="() => goto(maxPage)">{{ maxPage }}</button>
    <button
      :class="{
        'pagination__page': true,
        'pagination__page--disabled': _page >= maxPage,
      }"
      @click="() => _page < maxPage ? goto(_page + 1) : null"
    >
      &rarr;
    </button>
  </div>
</template>

<script>
const VISIBLE_PAGES = 5

export default {
  name: 'Pagination',
  props: {
    page: { type: Number, required: true },
    maxPage: { type: Number, required: true },
    visiblePages: { type: Number, default: VISIBLE_PAGES },
  },
  computed: {
    _page() {
      return Math.max(1, Math.min(this.maxPage, this.page))
    },
    from() {
      return Math.max(0, Math.min(this.maxPage - this.visiblePages - 2, this._page - Math.ceil(this.visiblePages / 2)))
    },
    to() {
      return Math.min(this.maxPage, Math.max(this.visiblePages + 2, this._page + Math.floor(this.visiblePages / 2)))
    },
  },
  methods: {
    goto(page) {
      if (page === this._page) { return false }

      const query = { ...this.$route.query }
      page > 1 ? query.page = page : delete query.page
      this.$router.push(
        {
          name: this.$route.name,
          params: this.$route.params,
          query,
        },
        async() => {
          if (this.$listeners.change) {
            await this.$listeners.change()
          } else {
            this.$router.go()
          }
        },
      )
    },
  },
}
</script>
