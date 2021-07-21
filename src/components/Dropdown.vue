<template>
    <div>
        <button @click="toggle" class="my-dropdown-button">{{title}}</button>
        <div class="my-dropdown-container" v-if="showDropdown">
            <button v-for="option in options" @click="selected(option)" class="my-dropdown-item">{{option}}</button>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {
        name: 'Dropdown',
        components: {},
        props: ['title', 'options',
            'defaultOption',
        ],
        data: function() {
            return {
                selectedItem: this.defaultOption,
                showDropdown: false,
            }
        },
        methods: {
            toggle: function() {
                this.showDropdown = !this.showDropdown
            },
            selected: function(option) {
                this.selectedItem = option
                this.$emit("setSelectedOption", option)
                this.toggle()
            }
        },
        mounted: function() {
            this.$emit("setSelectedOption",
                this.selectedItem)
        }
    }
</script>

<style type="text/css">
    .my-dropdown-button {
        position: relative;
        border-radius: 5px;
        border: none;
        background-color: var(--bs-secondary);
        color: var(--bs-light);
        text-align: center;
        margin-top: 2px;
        margin-bottom: 2px;
        margin-right: 2px;
        margin-left: 2px;
    }

    .my-dropdown-container {
        position: fixed;
        background-color: var(--bs-light);
        min-width: 50px;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        padding: 4px 4px;
        z-index: 4;
        border-radius: 5px;
        border: 2px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        overflow: visible;
    }

    .my-dropdown-item {
        transition-duration: 0.4s;
        border-radius: 5px;
        border: none;
        background-color: var(--bs-light);
        color: var(--bs-secondary);


    }

    .my-dropdown-item:hover {
        background-color: var(--bs-secondary);
        color: var(--bs-light);
    }

    .my-my-dropdown-item:focus {
        background-color: var(--bs-secondary);
        color: var(--bs-light);
    }
</style>