<template>
  <div class="main-title">
    <h1 class="main-title__header">{{ title }}</h1>
    <div class="main-title__subtitle">
      <span v-for="(link, name, index) in subtitle" :key="index" class="main-title__subtitle-item">
        <nuxt-link
          :class="{
            'main-title__subtitle-item-link': true,
            'main-title__subtitle-item-link--disabled': link === $nuxt.$route.path,
          }"
          :to="link"
          :event="link === $nuxt.$route.path ? '' : 'click'"
        >
          {{ name }}
        </nuxt-link>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  props: {
    title: { type: String, required: true },
    subtitle: { type: Object, default: () => {} },
  },
}
</script>
