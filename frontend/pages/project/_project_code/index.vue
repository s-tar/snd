<script>
import Listing from '~/components/Listing'

export default {
  extends: Listing,
  data() {
    return {
      project: {},
      categories: {},
    }
  },
  computed: {
    mainTitle() {
      return 'Categories'
    },
    mainButtons() {
      return [
        {
          name: 'Create',
          url: `/project/${this.project.code}/category/create`,
          class: 'button button--info',
        },
      ]
    },
    breadcrumbs() {
      return {
        [this.project.name]: `/project/${this.project.code}`,
      }
    },
    maxPage() {
      return this.categories.max_page
    },
    items() {
      const router = this.$router
      return this.categories.items.map((category) => {
        return {
          id: category.id,
          icon: 'fas fa-boxes',
          badges: this.getBadges(category),
          title: category.name,
          description: category.description,
          isFavorite: category.isFavorite,
          active: true,
          click: () => router.push(`/project/${this.project.code}/category/${category.code}`),
          actions: [
            {
              icon: category.isFavorite ? 'fas fa-star' : 'far fa-star',
              type: 'info',
              caption: '',
              action: () => this.toggleFavorite(category.id),
            },
            {
              icon: 'far fa-edit',
              type: 'info',
              caption: '',
              action: () => router.push(`/project/${this.project.code}/category/${category.code}/edit`),
            },
            {
              icon: 'fas fa-clipboard-list',
              type: 'info',
              caption: '',
              action: () => router.push({
                path: '/logs',
                query: { project: this.project.code, category: category.code },
              }),
            },
            {
              icon: 'fas fa-times',
              type: 'danger',
              caption: '',
              confirmation: {
                title: 'Delete category',
                text: 'Are you sure you want to delete this category?',
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
      } = this.$route.params
      this.project = await this.$axios.$get(`/project/${projectCode}`)
      await this.loadCategories()
    },

    getBadges(category) {
      const badges = []
      if (category.isFavorite) { badges.push({ icon: 'fas fa-star' }) }
      return badges
    },

    async pageChange() {
      await this.loadCategories()
    },

    async loadCategories() {
      const { page } = this.$route.query
      this.categories = await this.$axios.$get(
        `/project/${this.$route.params.project_code}/category/all`,
        { params: { page } },
      )
    },

    getDeleteUrl(id) {
      const category = this.categories.items.find(category => category.id === id)
      return `/project/${this.project.code}/category/${category.code}`
    },

    async toggleFavorite(id) {
      const categoryIndex = this.categories.items.findIndex(category => category.id === id)
      const isFavorite = this.categories.items[categoryIndex].isFavorite
      const favoriteType = 1
      if (!isFavorite) {
        await this.$axios.$post(
          'favorites/add', { entity_id: id, type: favoriteType },
        )
      } else {
        await this.$axios.$delete(
          'favorites/remove', { data: { entity_id: id, type: favoriteType } },
        )
      }
      const category = this.categories.items[categoryIndex]
      category.isFavorite = !isFavorite
      this.$set(this.categories.items, categoryIndex, category)
    },
  },
}
</script>
