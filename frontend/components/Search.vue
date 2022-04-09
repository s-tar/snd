<template>
  <div class="search">
    <input class="search__input" name="search_phrase" v-model="searchPhrase" @keypress="onKeypress" :placeholder="placeholder"/>
    <button class="search__button" v-if="withButton" @click="search">
      <i class="fa-solid fa-magnifying-glass"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    phrase: { type: String },
    placeholder: { type: String },
    onSearch: { type: Function, required: true },
    withButton: { type: Boolean, default: true },
  },
  data() {
    return {
      searchPhrase: this.phrase,
    }
  },
  methods: {
    search() {
      this.onSearch(this.searchPhrase)
    },
    onKeypress(e) {
      if (e.key === 'Enter') {
        this.search()
      }
    },
  },
}
</script>
