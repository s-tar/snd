export default {
  // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
  ssr: false,

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    title: 'Seek & Destroy',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { hid: 'og-title', property: "og:title", content: "Seek & Destroy" },
      { hid: 'og-description', property: "og:description", content: "Список военных преступников участвующих в войне в Украине" },
      { hid: 'og-image', property: "og:image", content: process.env.BASE_URL + "/ogicon_b.png" },
      { hid: 'og-type', property: "og:type", content: "website" },
      { hid: 'og-url', property: "og:url", content: process.env.BASE_URL }
    ],
    __dangerouslyDisableSanitizers: ['script', 'innerHTML'],
    script: [
      { src: 'https://www.googletagmanager.com/gtag/js?id=' + process.env.GOOGLE_ANALYTICS_CODE, defer: true },
      {
        innerHTML: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${process.env.GOOGLE_ANALYTICS_CODE}');
        `,
        type: 'text/javascript',
        charset: 'utf-8',
      },
      { src: 'https://use.fontawesome.com/releases/v6.1.1/js/all.js', defer: true, integrity: 'sha384-xBXmu0dk1bEoiwd71wOonQLyH+VpgR1XcDH3rtxrLww5ajNTuMvBdL5SOiFZnNdp', crossorigin: 'anonymous' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.png' },
      {
        as: 'style',
        rel: 'stylesheet preload prefetch',
        href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
      },
    ]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [
    "@assets/style/style.styl"
  ],
  webfontloader: {
    google: {
      families: [
        'Roboto:300,400,500,700',
      ]
    }
  },
  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    { src: '~/plugins/vue-flagpack.js', mode: 'client' },
    { src: '~/plugins/v-viewer', mode: 'client' },
    { src: '~/plugins/vue-advanced-cropper', mode: 'client' },
    { src: '~/plugins/datepicker', mode: 'client' },
    '~/plugins/axios',
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    '@nuxtjs/eslint-module',
    '@nuxtjs/style-resources',
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    'nuxt-webfontloader',
  ],
  styleResources: {
    stylus: [
      '@/assets/styl/style.styl',
    ],
  },
  publicRuntimeConfig: {
    axios: {
      browserBaseURL: process.env.API_URL,
    }
  },
  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    progress: false,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS',
    },
  },
  router: {
    base: process.env.BASE_PATH,
    middleware: ['auth']
  },
  auth: {
    localStorage: false,
    redirect: {
      login: '/auth/login',
      logout: '/auth/logout',
      home: '/',
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: 'auth/login', method: 'post', propertyName: 'access_token' },
          user: { url: 'user/me', method: 'get', propertyName: '' },
          logout: false,
        }
      }
    }
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {
    extractCSS: true,
    cssSourceMap: true,
    optimizeCSS: true,
    babel:{
      plugins: [
        ['@babel/plugin-proposal-private-methods', { loose: true }]
      ]
    },
    filenames: {
      app: ({ isDev }) => isDev ? '[name].js' : '[contenthash].js',
      // chunk: ({ isDev }) => isDev ? '[name].js' : '[contenthash].js',
      css: ({ isDev }) => isDev ? '[name].css' : '[contenthash].css',
      // img: ({ isDev }) => isDev ? '[path][name].[ext]' : 'img/[contenthash:7].[ext]',
      // font: ({ isDev }) => isDev ? '[path][name].[ext]' : 'fonts/[contenthash:7].[ext]',
      // video: ({ isDev }) => isDev ? '[path][name].[ext]' : 'videos/[contenthash:7].[ext]'
    }
  }
}
