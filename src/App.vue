<template>
    <h1> {{title}} </h1>
    <p>
        <input type="text" ref="name">
        <button @click='handleClick'>Click Me</button>
    </p>
    <Modal />
</template>

<script>
    import Modal from './components/Modal.vue'
    export default {
        name: 'App',
        components: {
            Modal
        },
        data() {
            return {
                title: 'My first view app '
            }
        },
        methods: {
            handleClick() {
                console.log(this.$refs.name)
                this.$refs.name.classList.add('active')
                this.$refs.name.focus()
            }
        }
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
</style>