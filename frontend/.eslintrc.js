module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    "vue/multi-word-component-names": "off",
    "vue/singleline-html-element-content-newline": "off",
    "comma-dangle": [2, "always-multiline"],
    "space-before-function-paren": ["error", "never"],
    "vue/html-self-closing": ["error", {
      "html": {
        "void": "always",
        "normal": "never",
      },
    }]
  }
}
