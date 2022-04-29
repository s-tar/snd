<script>
import Listing from '~/components/Listing'
import PersonCard from '~/components/Listing/ListItems/PersonCard'

export default {
  extends: Listing,
  auth: false,
  data() {
    return {
      persons: {},
      units: {},
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
    maxPage() {
      return this.persons.max_page
    },
    items() {
      return this.persons.items.map((person, index) => {
        if (person.military && person.military.unit) {
          person.military.unitData = this.units[person.military.unit]
        }
        return {
          id: person.code,
          icon: 'fa-solid fa-user',
          title: `${person.last_name} ${person.first_name}  ${person.middle_name || ''}`,
          person,
          description: person.birthday,
          active: true,
          click: () => {
            this.getToggleFullInfo(index)
          },
          actions: [],
        }
      })
    },
    unitIds() {
      const unitIds = new Set()
      this.persons.items.forEach((person) => {
        if (person.military && person.military.unit) {
          unitIds.add(person.military.unit)
        }
      })
      return [...unitIds]
    },
  },
  methods: {
    async init() {
      this.persons = await this.loadPersons()
      if (this.unitIds.length > 0) {
        this.units = await this.loadMilitaryUnits(this.unitIds)
      }
      this.loading = false
    },
    async pageChange() {
      window.scrollTo(0, 0)
      this.loading = true
      this.persons = await this.loadPersons()
      if (this.unitIds.length > 0) {
        this.units = await this.loadMilitaryUnits(this.unitIds)
      }
      this.loading = false
    },
    async loadMilitaryUnits(ids) {
      const res = await this.$axios.$get(
        '/unit/get',
        {
          params: { ids },
          paramsSerializer: params => require('qs').stringify(params, { arrayFormat: 'repeat' }),
        },
      )
      const units = {}
      res.items.forEach((unit) => { units[unit.id] = unit })
      return units
    },
    async loadPersons() {
      const { page, s } = this.$route.query
      return await this.$axios.$get(
        '/person/all',
        { params: { page, s } },
      )
    },
    getToggleFullInfo(index) {
      const person = this.persons.items[index]
      person.showFullInfo = !person.showFullInfo
      this.$set(this.persons.items, index, person)
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
