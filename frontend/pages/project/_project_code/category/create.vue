<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle title="Category: New" />
    </div>
    <CategoryForm :project-code="project.code" />
  </div>
</template>

<script>
import CategoryForm from '~/components/forms/CategoryForm'

export default {
  components: {
    CategoryForm,
  },
  async fetch() {
    try {
      const {
        project_code: projectCode,
      } = this.$route.params

      this.project = await this.$axios.$get(`/project/${projectCode}`)
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
      project: null,
      loading: true,
    }
  },
}
</script>
