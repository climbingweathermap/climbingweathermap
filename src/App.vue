<template>
    <h1>{{title}}</h1>
    <br>
    <button @click='toggleModal'>Click Me</button>
    <div v-if="showModal">
        <Modal @closeModal='toggleModal' :header="modal_header" :text="modal_text" :theme="modal_theme" />
    </div>
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
                title: 'My first view app',
                modal_header: "HELLO!",
                modal_text: "World!!",
                modal_theme: "highlight",
                showModal: false
            }
        },
        methods: {
            toggleModal() {
                this.showModal = !this.showModal
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