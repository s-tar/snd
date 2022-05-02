<template>
    <header class="header">
      <div class="header_content container container--separated container--centered">
        <div class="header__title">
          <a class="header__logo" href="/">Seek<small>&</small>Destroy</a>
          <a class="header__logo header__logo--mobile" href="/">S&D</a>
        </div>
        <div class="header__menu">
          <div><a href="/" class="link">Главная</a></div>
          <div>
            <div v-if="isAuth" class="header__profile">
              <div>{{ $auth.user.name }}</div>
              <a href="/auth/logout" class="link">Выход</a>
            </div>
            <a v-else href="/auth/login" class="link">Вход</a>
          </div>
        </div>
      </div>
    </header>
</template>

<script>
export default {
  computed: {
    isAuth() {
      return !!this.$auth.user
    },
  },
}
</script>
