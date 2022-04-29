<template>
  <div v-if="loading">Loading...</div>
  <PersonForm
    v-else-if="!$fetchState.pending"
    :id="person.id"
    json
    :data="person"
    action="/person/update"
  />
</template>

<script>
import PersonForm from '~/components/forms/PersonForm'

export default {
  components: {
    PersonForm,
  },
  data() {
    return {
      loading: true,
      person: {},
    }
  },
  async fetch() {
    if (this.$auth.user && this.$auth.user.role < 2) {
      return this.$router.push({ path: '/' })
    }

    try {
      const { person_code: personCode } = this.$route.params
      const response = await this.$axios.$get(`/person/${personCode}`)
      this.person = response.person
      if (this.person.military && this.person.military.unit) {
        const response = await this.$axios.$get(
          '/unit/get',
          {
            params: { ids: [this.person.military.unit] },
            paramsSerializer: params => require('qs').stringify(params, { arrayFormat: 'repeat' }),
          },
        )
        this.person.military.unit = response.items.pop()
      }
      this.loading = false
    } catch (e) {
      return this.$nuxt.error({
        statusCode: e.response.status,
        message: e.response.statusText,
      })
    }
  },
  computed: {
    title() {
      return [this.person.last_name, this.person.first_name, this.person.middle_name].join(' ')
    },
  },
}
</script>
