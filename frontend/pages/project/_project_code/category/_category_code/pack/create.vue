<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle title="Pack: New" />
    </div>
    <PackForm :project-code="project.code" :category-code="category.code" :platforms="platforms" />
  </div>
</template>

<script>
import PackForm from '~/components/forms/PackForm'

export default {
  components: {
    PackForm,
  },
  async fetch() {
    try {
      const {
        project_code: projectCode,
        category_code: categoryCode,
      } = this.$route.params

      this.platforms = await this.$axios.$get('/platforms')
      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.category = await this.$axios.$get(`/project/${projectCode}/category/${categoryCode}`)
      this.loading = false
    } catch (e) {
      return this.$nuxt.error({
        statusCode: e.response.status,
        message: e.response.statusText,
      })
    }
  },
  data() {
    return {
      platforms: {},
      project: null,
      category: null,
      loading: true,
    }
  },
}
</script>
