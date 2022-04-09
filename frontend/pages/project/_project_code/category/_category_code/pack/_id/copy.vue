<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle :title="`Pack #${pack.id}: Copy`" />
    </div>
    <PackCopyForm
      :project-code="project.code"
      :category-code="category.code"
      :pack-id="pack.id"
      :categories="categories.items"
      :description="`[Copy] ${pack.description}`"
    />
  </div>
</template>

<script>
import PackCopyForm from '~/components/forms/PackCopyForm'

export default {
  components: {
    PackCopyForm,
  },
  async fetch() {
    try {
      const {
        project_code: projectCode,
        category_code: categoryCode,
        id,
      } = this.$route.params

      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.category = await this.$axios.$get(`/project/${projectCode}/category/${categoryCode}`)
      this.categories = await this.$axios.$get(
        `/project/${projectCode}/category/all`, {
          params: { per_page: 999 },
        },
      )
      this.pack = await this.$axios.$get(
        `/project/${projectCode}/category/${categoryCode}/pack/${id}`, {
          params: { with_bundles: true },
        },
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
      categories: [],
      pack: {},
    }
  },
}
</script>
