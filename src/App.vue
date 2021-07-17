<template>
    <div class="content">
        <NavBar />
        <div class="row">
            <div class="col">
                <SideBar />
            </div>
            <div class="col">
                <Map />
            </div>
        </div>
        <teleport to=".footer">
            <Footer />
        </teleport>
    </div>
</template>

<script>
    import Modal from './components/Modal.vue'
    import NavBar from './components/NavBar.vue'
    import SideBar from './components/SideBar.vue'
    import Map from './components/Map.vue'
    import Footer from './components/Footer.vue'
    export default {
        name: 'App',
        components: {
            Modal,
            NavBar,
            SideBar,
            Map,
            Footer
        }
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        ;
    }
</style>