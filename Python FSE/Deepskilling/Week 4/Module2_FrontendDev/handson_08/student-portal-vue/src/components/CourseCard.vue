<template>
  <article class="course-card">
    <h3>{{ name }}</h3>
    <p>{{ code }}</p>
    <span>{{ credits }} credits</span>
    <p>Grade: {{ grade }}</p>
  </article>
</template>

<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String
});
</script>

<style scoped>
.course-card {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>