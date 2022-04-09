<template>
  <div class="profile">
    <div class="profile__info">
      <div class="profile__name">{{ user.name }}</div>
      <button v-if="user.id" class="link" @click="logout">Logout</button>
      <a v-if="!user.id" class="link" href="/auth/login">Login</a>
    </div>
    <div v-if="false" class="profile__photo">
      <i class="fa-solid fa-user"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data() {
    return {
    }
  },
  computed: {
    user() {
      return this.$auth.user || {}
    },
  },
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push('/')
    },
  },
}
</script>
