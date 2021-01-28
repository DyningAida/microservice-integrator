//register component
Vue.component('login',{
  template: '#template-login',

}), 
Vue.component('home',{
    template: '#template-home',
    computed: {
        state() {
          return this.name.length >= 4
        },
        invalidFeedback() {
          if (this.name.length > 0) {
            return 'Enter at least 4 characters.'
          }
          return 'Please enter something.'
        }
      },
    data(){
        return{
            name:''
        }
    }
}),
Vue.component('nilai',{
    template: '#template-nilai',
    data(){
        return{
          items: [
              { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
              { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
              { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
              { age: 38, first_name: 'Jami', last_name: 'Carney' }
            ]
        }     
      }
}),
Vue.component('keuangan',{
  template: '#template-keuangan',
  data(){
    return{
      items: [
          { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
          { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
          { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
          { age: 38, first_name: 'Jami', last_name: 'Carney' }
        ]
    }     
  }
}),

Vue.component('dosen',{
  template:'#template-dosen',
  data(){
    return{
      items: [
          { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
          { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
          { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
          { age: 38, first_name: 'Jami', last_name: 'Carney' }
        ]
    }     
  }
}),

Vue.component('asset',{
  template: '#template-asset',
  data(){
    return{
      items: [
          { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
          { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
          { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
          { age: 38, first_name: 'Jami', last_name: 'Carney' }
        ]
    }     
  }
}),

Vue.component('jadwal', {
  template: '#template-jadwal',
  data(){
    return{
      items: [
          { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
          { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
          { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
          { age: 38, first_name: 'Jami', last_name: 'Carney' }
        ]
    }     
  }
}),

Vue.component('profil',{
  template: '#template-profil',
  data(){
    return{
      items:[
        { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
          { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
          { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
          { age: 38, first_name: 'Jami', last_name: 'Carney' }
      ]
    }
  }
})

new Vue({
    el : '#app',
    data: {
      username:'',
      numbers : [1,2,3,4,5],
      currentView : 'home',
    }
    ,
    methods:{
      caribilangangenap: function(numbers){
        return numbers.filter(i => {
          return i % 2 == 0
        })
      }
    },
})