<template>
  <div v-if="loading">Loading...</div>
  <div v-else>
    <div class="container container--separated container--v-centred">
      <MainTitle
        :title="`Pack: #${pack.id }`"
        :subtitle="{
          [project.name]: `/project/${project.code}`,
          [category.name]: `/project/${project.code}/category/${category.code}`,
        }"
      />
      <div class="buttons">
        <nuxt-link :to="`/project/${project.code}/category/${category.code}/pack/${pack.id}/copy`" class="button button--info">
          <span class="fas fa-clone"></span> Copy
        </nuxt-link>
        <nuxt-link :to="`/project/${project.code}/category/${category.code}`" class="button button--info">Back</nuxt-link>
      </div>
    </div>
    <div class="card">
      <div class="card__body">
        <div class="form">
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Description</div>
            <div class="form__field form__field--readonly">{{ pack.description }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Platform</div>
            <div class="form__field form__field--readonly">{{ pack.platform }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Created at</div>
            <div class="form__field form__field--readonly">{{ formatDateTime(pack.createdAt) }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Size</div>
            <div class="form__field form__field--readonly">{{ bytesToString(size) }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Hash</div>
            <div class="form__field form__field--readonly">{{ pack.hash }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">URL</div>
            <div class="form__field form__field--readonly">{{ pack.url }}</div>
          </div>
          <div class="form__row">
            <div class="form__field-label form__field-label--upper">Bundles</div>
            <div class="form__field form__field--no-underline">
              <div class="list list--table">
                <div class="list__item list__item--table-row list__item-cell--size-s">
                  <div class="list__item-cell"><b>Name</b></div>
                  <div class="list__item-cell"><b>Compression</b></div>
                  <div class="list__item-cell"><b>Hash</b></div>
                  <div class="list__item-cell"><b>Size</b></div>
                  <div class="list__item-cell"><b>Link</b></div>
                </div>
                <div v-for="bundle in orderedBundles" :key="bundle.name" class="list__item list__item--table-row list__item-cell--size-s">
                  <div class="list__item-cell">{{ bundle.name }}</div>
                  <div class="list__item-cell">{{ bundle.compression }}</div>
                  <div class="list__item-cell" :title="bundle.hash">{{ bundle.hash ? shortHash(bundle.hash) : '' }}</div>
                  <div class="list__item-cell">{{ bytesToString(bundle.size) }}</div>
                  <div class="list__item-cell">
                    <a :href="bundle.url" class="link" :title="bundle.url"><i class="fas fa-cloud-download-alt"></i></a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDateTime } from '~/utils/datetime'

export default {
  async fetch() {
    try {
      const {
        project_code: projectCode,
        category_code: categoryCode,
        id,
      } = this.$route.params

      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.category = await this.$axios.$get(
        `/project/${projectCode}/category/${categoryCode}`,
      )
      this.pack = await this.$axios.$get(
        `/project/${projectCode}/category/${categoryCode}/pack/${id}`, {
          params: { with_bundles: true },
        },
      )
      this.loading = false
    } catch (e) {
      return this.$nuxt.error({
        statusCode: e.response.status,
        message: e.response.statusText,
      })
    }
  },
  data() {
    return {
      loading: true,
      project: null,
      category: null,
      pack: null,
    }
  },
  computed: {
    size() {
      let size = 0
      for (const bundle of this.pack.bundles) {
        size += bundle.size
      }
      return size
    },
    orderedBundles() {
      return [...this.pack.bundles].sort((a, b) => (a.name > b.name) ? 1 : -1)
    },
  },
  methods: {
    formatDateTime,
    shortHash(hash) {
      return `${hash.substring(0, 5)}...${hash.substr(-5)}`
    },
    bytesToString(bytes) {
      const multiplies = {
        TB: 1e12,
        GB: 1e9,
        MB: 1e6,
        kB: 1e3,
        B: 1,
      }
      for (const [name, mult] of Object.entries(multiplies)) {
        if (bytes / mult > 1) {
          return `${Math.round(bytes * 10 / mult) / 10}${name}`
        }
      }
    },
  },
}
</script>
