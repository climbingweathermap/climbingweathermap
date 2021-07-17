<template>
    <div class="content">
        <teleport to=".navb">
            <NavBar />
        </teleport>
        <teleport to=".footer">
            <Footer />
        </teleport>
        <div class="row align-left">
            <div class="col-sm">
                <SideBar />
            </div>
            <div class="col-xxl align-left">
                <Map />
            </div>
        </div>
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