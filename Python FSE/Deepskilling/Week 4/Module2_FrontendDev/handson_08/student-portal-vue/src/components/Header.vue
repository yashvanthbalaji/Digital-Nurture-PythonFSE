<template>
  <header class="header">
    <div class="site-name">Student Portal</div>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <div class="enrolled-count">Enrolled: {{ store.enrolledCourses.length }}</div>
  </header>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #2c3e50;
  color: #fff;
}
.header nav a {
  color: #fff;
  text-decoration: none;
  margin-right: 16px;
}
</style>