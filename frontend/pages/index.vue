<script>
import Listing from '~/components/Listing'
import PersonCard from '~/components/Listing/ItemsList/PersonCard'

export default {
  extends: Listing,
  auth: false,
  data() {
    return {
      persons: {},
      squads: {},
    }
  },
  computed: {
    withSearch() { return true },
    mainTitle() {
      return ''
    },
    itemsListComponent() {
      return PersonCard
    },
    mainButtons() {
      return [
        // {
        //   name: 'Add Person',
        //   url: '/person/add',
        //   class: 'button button--success',
        // },
      ]
    },
    maxPage() {
      return this.persons.max_page
    },
    items() {
      return this.persons.items.map((person, index) => {
        return {
          id: person.code,
          icon: 'fa-solid fa-user',
          title: `${person.last_name} ${person.first_name}  ${person.middle_name} `,
          person,
          squad: person.military ? this.squads[person.military.squad] : null,
          description: person.birthday,
          active: true,
          click: () => {
            this.getToggleFullInfo(index)
          },
          actions: [],
        }
      })
    },
    squadIds() {
      const squadIds = new Set()
      this.persons.items.forEach((person) => {
        if (person.military && person.military.squad) {
          squadIds.add(person.military.squad)
        }
      })
      return [...squadIds]
    },
  },
  methods: {
    async init() {
      this.persons = await this.loadPersons()
      if (this.squadIds.length > 0) {
        this.squads = await this.loadSquads(this.squadIds)
      }
      this.loading = false
    },
    async pageChange() {
      window.scrollTo(0, 0)
      this.loading = true
      this.persons = await this.loadPersons()
      if (this.squadIds.length > 0) {
        this.squads = await this.loadSquads(this.squadIds)
      }
      this.loading = false
    },
    async loadSquads(ids) {
      const res = await this.$axios.$get(
        '/squads/get',
        {
          params: { ids },
          paramsSerializer: params => require('qs').stringify(params, { arrayFormat: 'repeat' }),
        },
      )
      return res.squads
    },
    async loadPersons() {
      const { page, s } = this.$route.query
      return await this.$axios.$get(
        '/persons/all',
        { params: { page, s } },
      )
    },
    getToggleFullInfo(index) {
      const person = this.persons.items[index]
      person.showFullInfo = !person.showFullInfo
      this.$set(this.persons.items, index, person)
    },
    getDeleteUrl(id) {
      const person = this.persons.findIndex(person => person.id === id)
      return `/project/${person.code}`
    },
    onSearch(phrase) {
      this.$router.push(
        {
          name: this.$route.name,
          query: { s: phrase },
        },
        () => {
          this.$router.go()
        },
      )
    },
  },
}
</script>
