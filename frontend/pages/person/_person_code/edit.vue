<template>
  <div v-if="loading">Loading...</div>
  <PersonForm
     v-else-if="!$fetchState.pending"
     json
     :id="person.id"
     :data="person"
  />
</template>

<script>
import PersonForm from '~/components/forms/PersonForm'

export default {
  components: {
    PersonForm,
  },
  async fetch() {
    try {
      const { person_code: personCode } = this.$route.params
      const response = await this.$axios.$get(`/person/${personCode}`)
      this.person = response.person
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
      return [this.person.last_name, this.person.first_name, this.person.middle_name].join(' ')
    },
  },
}
</script>
