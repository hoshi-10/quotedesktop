<template>

  <el-table :data="list" border>

    <el-table-column prop="id" label="序号" width="60" />
    <el-table-column prop="content" label="内容" />
    <el-table-column prop="quantity" label="数量" />
    <el-table-column prop="price" label="价格" />
    <el-table-column prop="subtotal" label="总价" />
    <el-table-column prop="material" label="材料" />
    <el-table-column prop="size" label="规格尺寸" />
    <el-table-column prop="handler" label="经办人" />
    <el-table-column prop="remark" label="备注" />

    <el-table-column label="操作" width="100">
      <template #default="scope">
        <el-button
          type="danger"
          size="small"
          @click="deleteItem(scope.row)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>

  </el-table>

</template>

<script setup>
import { ref, onMounted } from 'vue'

const list = ref([])

onMounted(async () => {
  const result = await window.api.readExcel()
  list.value = result
})

/* 重排序号 */
const resetIndex = () => {
  list.value.forEach((item, index) => {
    item.id = index + 1
  })
}

/* 删除 */
const deleteItem = async (row) => {
  list.value = list.value.filter(item => item.id !== row.id)
  resetIndex()
  await window.api.saveExcel(list.value)
}
</script>