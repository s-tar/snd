<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle :title="`Category: ${category.name}`" />
    </div>
    <CategoryForm
      :project-code="project.code"
      :code="category.code"
      :name="category.name"
      :description="category.description"
    />
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
        category_code: categoryCode,
      } = this.$route.params

      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.category = await this.$axios.$get(
        `/project/${projectCode}/category/${categoryCode}`,
      )
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
      loading: true,
      project: {},
      category: {},
    }
  },
}
</script>
