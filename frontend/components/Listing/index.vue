<template>
  <div v-if="loading" class="loading"></div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle :title="mainTitle" :subtitle="breadcrumbs" />
      <div class="buttons">
        <nuxt-link v-for="(button, index) in mainButtons" :key="index" :to="button.url" :class="button.class">{{ button.name }}</nuxt-link>
      </div>
    </div>
    <div class="container container--separated container--v-centred">
      <a v-if="canAdd" href="/person/add" class="button button--success button--add-person">
        <i class="fa-solid fa-user-plus"></i>
        <span class="button__text button__text--desktop">Добавить</span>
      </a>
      <div v-if="onSearch" class="card search-wrapper">
        <div class="card__body">
          <Search :phrase="$nuxt.$route.query['s']" placeholder="Поиск" :on-search="onSearch" />
        </div>
      </div>
    </div>
    <div v-if="Object.keys(filters).length > 0" class="card">
      <AsyncForm
        ref="form"
        action=""
        method="GET"
        class="form form--direction-horizontal"
      >
        <div v-for="(filter, key) in filters" :key="key" class="form__col">
          <SelectField
            :id="key"
            :name="key"
            :label="filter.name"
            :value="filter.value ? filter.value : $nuxt.$route.query[key]"
            :readonly="filter.disabled === true"
            @change="(e) => onFilterChange(e, filter.change)"
          >
            <option v-for="([optionKey, value]) in processFilterValues(filter.values)" :key="optionKey" :value="optionKey">{{ value }}</option>
          </SelectField>
        </div>
      </AsyncForm>
    </div>
    <div v-if="total > 0" class="search-general-info">Найдено: {{ total }}</div>
    <component
      :is="itemsListComponent"
      v-for="(item, i) in visibleItems"
      :key="i"
      :item="item"
    />
    <div v-if="visibleItems.length == 0">
      Ничего не найдено.
    </div>
    <div class="container container--centred">
      <Pagination :page="page" :max-page="maxPage" :visible-pages="visiblePages" @change="pageChange" />
    </div>
  </div>
</template>

<script>
import Card from './ListItems/Card'
import MainTitle from '~/components/MainTitle'
import Pagination from '~/components/Pagination'
import SelectField from '~/components/AsyncForm/fields/Select'
import Search from '~/components/Search'

export default {
  components: {
    MainTitle,
    Pagination,
    SelectField,
    Search,
  },
  data() {
    return {
      loading: true,
      deleted: {},
      searchPhrase: '',
      screenWidth: 0,
    }
  },
  async fetch() {
    try {
      await this.init()
      this.loading = false
    } catch (e) {
      return this.$nuxt.error({
        statusCode: e.response.status,
        message: e.response.statusText,
      })
    }
  },
  computed: {
    canAdd() {
      return this.$auth.user && this.$auth.user.role > 1
    },
    visiblePages() {
      return this.screenWidth > 500 ? 5 : 2
    },
    itemsListComponent() {
      return Card
    },
    mainTitle() {
      return ''
    },
    mainButtons() {
      return []
    },
    breadcrumbs() {
      return {}
    },
    filters() {
      return {}
    },
    items() {
      return []
    },
    total() {
      return 0
    },
    page() {
      const page = parseInt(this.$route.query.page)
      return isNaN(page) ? 1 : page
    },
    maxPage() {
      return 1
    },
    visibleItems() {
      return this.items.filter(item => !this.deleted[item.id])
    },
    withSearch() { return false },
  },
  beforeMount() {
    window.addEventListener('resize', this.onResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize)
  },
  created() {
    this.screenWidth = this.getScreenWidth()
  },
  methods: {
    async init() {},
    async pageChange() {},
    async onSearch() {},
    getDeleteUrl(id) { throw new Error('Unimplemented') },
    getScreenWidth() {
      return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
    },
    onResize() {
      this.screenWidth = this.getScreenWidth()
    },
    onFilterChange(e, action) {
      const { name, value } = e.target
      const query = { ...this.$route.query }
      value ? query[name] = value : delete query[name]
      this.$router.push(
        {
          name: this.$route.name,
          params: this.$route.params,
          query,
        },
        async() => {
          if (action) {
            await action(e)
          } else {
            this.$router.go()
          }
        },
      )
    },
    processFilterValues(values) {
      if (values instanceof Map) {
        return values
      } else if (values instanceof Object) {
        return Object.entries(values)
      } else {
        return values
      }
    },
    onDelete(id) {
      this.$axios.$delete(this.getDeleteUrl(id))
        .then(() => {
          this.$set(this.deleted, id, true)
          this.$nuxt.$emit('modal-close')
        })
        .catch((e) => {
          return this.$nuxt.error({
            statusCode: e.response.status,
            message: e.response.statusText,
          })
        })
    },
  },
}
</script>
