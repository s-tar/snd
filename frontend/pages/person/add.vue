<template>
  <div>
    <div class="container container--separated container--v-centred">
      <MainTitle title="Add person" />
    </div>
    <PersonForm :person="{}" />
  </div>
</template>

<script>
import PersonForm from '~/components/forms/PersonForm'

export default {
  components: {
    PersonForm,
  },
}
</script>
