export default function({ $axios, redirect }) {
  $axios.onRequest((config) => {
    config.progress = false
  })
}
