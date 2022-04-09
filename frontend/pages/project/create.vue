<template>
  <div>
    <div class="container container--separated container--v-centred">
      <MainTitle title="Project: New" />
    </div>
    <ProjectForm />
  </div>
</template>

<script>
import ProjectForm from '~/components/forms/ProjectForm'

export default {
  components: {
    ProjectForm,
  },
}
</script>
