<template>
  <div>
    <div class="container container--separated container--v-centred">
      <MainTitle title="Add person" />
    </div>
    <PersonForm :data="{}" action="/person/add" />
  </div>
</template>

<script>
import PersonForm from '~/components/forms/PersonForm'

export default {
  components: {
    PersonForm,
  },
  fetch() {
    if (this.$auth.user && this.$auth.user.role < 2) {
      return this.$router.push({ path: '/' })
    }
  },
}
</script>
