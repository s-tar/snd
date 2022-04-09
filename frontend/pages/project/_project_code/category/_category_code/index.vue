<script>
import Listing from '~/components/Listing'

export default {
  extends: Listing,
  data() {
    return {
      project: {},
      category: {},
      packs: {},
      platforms: {},
    }
  },
  computed: {
    mainTitle() {
      return 'Packs'
    },
    mainButtons() {
      return [
        {
          name: 'Create',
          url: `/project/${this.project.code}/category/${this.category.code}/pack/create`,
          class: 'button button--info',
        },
      ]
    },
    breadcrumbs() {
      return {
        [this.project.name]: `/project/${this.project.code}`,
        [this.category.name]: `/project/${this.project.code}/category/${this.category.code}`,
      }
    },
    maxPage() {
      return this.packs.max_page
    },
    filters() {
      return {
        platform: {
          name: 'Platform',
          type: 'select',
          values: { '': 'Any', ...this.platforms },
          change: this.filterChange,
        },
        status: {
          name: 'Status',
          type: 'select',
          values: {
            '': 'Any',
            true: 'Active',
            false: 'Disabled',
          },
          change: this.filterChange,
        },
      }
    },
    items() {
      const router = this.$router
      return this.packs.items.map((pack) => {
        return {
          id: pack.id,
          icon: 'fas fa-box',
          title: `#${pack.id}: ${pack.platform}`,
          description: pack.description,
          active: pack.active,
          click: () => router.push(`/project/${this.project.code}/category/${this.category.code}/pack/${pack.id}`),
          actions: [
            {
              icon: pack.active ? 'fas fa-eye-slash' : 'fas fa-eye',
              type: 'info',
              caption: '',
              action: this.toggleActive,
            },
            {
              icon: 'fa fa-clone',
              type: 'info',
              caption: '',
              action: () => router.push(`/project/${this.project.code}/category/${this.category.code}/pack/${pack.id}/copy`),
            },
            {
              icon: 'fas fa-clipboard-list',
              type: 'info',
              caption: '',
              action: () => router.push({
                path: '/logs',
                query: { project: this.project.code, category: this.category.code, pack: pack.id },
              }),
            },
            {
              icon: 'fas fa-times',
              type: 'danger',
              caption: '',
              confirmation: {
                title: 'Delete pack',
                text: 'Are you sure you want to delete this pack?',
                action: this.onDelete,
              },
            },
          ],
        }
      })
    },
  },
  methods: {
    async init() {
      const {
        project_code: projectCode,
        category_code: categoryCode,
      } = this.$route.params

      this.platforms = await this.$axios.$get('/platforms')
      this.project = await this.$axios.$get(`/project/${projectCode}`)
      this.category = await this.$axios.$get(`/project/${projectCode}/category/${categoryCode}`)
      await this.loadPacks()
    },
    async pageChange() {
      await this.loadPacks()
    },
    async filterChange() {
      await this.loadPacks()
    },
    async loadPacks() {
      const {
        project_code: projectCode,
        category_code: categoryCode,
      } = this.$route.params
      const { platform, status, page } = this.$route.query
      this.packs = await this.$axios.$get(
        `/project/${projectCode}/category/${categoryCode}/pack/all`,
        { params: { with_bundles: false, platform, status, page } },
      )
    },
    getDeleteUrl(id) {
      return `/project/${this.project.code}/category/${this.category.code}/pack/${id}`
    },
    async toggleActive(id) {
      const packIndex = this.packs.items.findIndex(pack => pack.id === id)
      const active = this.packs.items[packIndex].active
      const {
        project_code: projectCode,
        category_code: categoryCode,
      } = this.$route.params

      const pack = await this.$axios.$put(
        `/project/${projectCode}/category/${categoryCode}/pack/${id}`,
        JSON.stringify({ active: !active }),
      )

      this.$set(this.packs.items, packIndex, pack)
    },
  },
}
</script>
