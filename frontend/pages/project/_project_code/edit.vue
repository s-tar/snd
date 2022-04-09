<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle :title="`Project: ${project.code}`" />
    </div>
    <ProjectForm
      v-if="!$fetchState.pending"
      :code="project.code"
      :name="project.name"
      :description="project.description"
    />
  </div>
</template>

<script>
import ProjectForm from '~/components/forms/ProjectForm'

export default {
  components: {
    ProjectForm,
  },
  async fetch() {
    try {
      const {
        project_code: projectCode,
      } = this.$route.params
      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.categories = await this.$axios.$get(`/project/${projectCode}/category/all`)
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
    }
  },
}
</script>
