<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle :title="`Person: ${project.code}`" />
    </div>
    <PersonForm
      v-if="!$fetchState.pending"
      :code="project.code"
      :name="project.name"
      :description="project.description"
    />
  </div>
</template>

<script>
import PersonForm from '~/components/forms/PersonForm'

export default {
  components: {
    PersonForm,
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
      person: {},
    }
  },
  computed: {
    title() {
      if (this.person.id) {
        return [this.person.lastname, this.person.firstname, this.person.middlename].join(' ')
      } else {
        return 'Add person'
      }
    }
  },
}
</script>
