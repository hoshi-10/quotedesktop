<template>
  <div>
<el-button type="success" @click="importExcel" style="margin-bottom:20px">
  导入Excel
</el-button>
    <!-- 合计 -->
    <h3>合计：{{ totalSum }}</h3>

    <!-- 表单 -->
    <el-form :model="form" label-width="80px">

      <el-form-item label="内容" required>
        <el-input v-model="form.content" />
      </el-form-item>

      <el-form-item label="数量" required>
        <el-input-number v-model="form.quantity" />
      </el-form-item>

      <el-form-item label="价格" required>
        <el-input-number v-model="form.price" />
      </el-form-item>

      <el-form-item label="总价">
        <el-input v-model="form.subtotal" disabled />
      </el-form-item>

      <el-form-item label="材料">
        <el-input v-model="form.material" />
      </el-form-item>

      <el-form-item label="规格尺寸">
        <el-input-number v-model="form.size" />
      </el-form-item>

      <el-form-item label="经办人">
        <el-input v-model="form.handler" />
      </el-form-item>

      <el-form-item label="备注">
        <el-input v-model="form.remark" />
      </el-form-item>

      <el-button type="primary" @click="addItem">
        添加
      </el-button>

    </el-form>
<ExcelTable :list="list" style="margin: 20px 0;" />
    <!-- 表格 -->
    <el-input
v-model="keyword"
placeholder="搜索内容"
style="margin-bottom:10px"
/>
    <el-table :data="filteredList" border style="margin-top:20px">

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
          <el-button
  size="small"
  @click="editItem(scope.row, scope.$index)"
>
  编辑
</el-button>
        </template>
      </el-table-column>

    </el-table>

  </div>
</template>

<script setup>
import { ref, reactive,onMounted, computed, watch } from 'vue'

/* 数据列表 */
const list = ref([])

/* 表单 */
const form = reactive({
  id: null,//序号，自动
  content: '',//内容
  quantity: null,//数量
  price: null,//价格
  subtotal: 0,//总价
  material: '',//材料
  size: null,//规格
  handler: '',//经办人
  remark: '',//备注
  image: ''//图片暂时空着
})
const importExcel = async () => {
  const data = await window.api.selectAndReadExcel()
  console.log('导入的数据:', data)

  if (data.length > 0) {
    list.value = data
  }
}
onMounted(async () => {
  const result = await window.api.readExcel()
  list.value = result
})

/* 监听自动计算总价 */
watch(
  () => [form.quantity, form.price],
  () => {
    if (form.quantity && form.price) {
      form.subtotal = form.quantity * form.price
    } else {
      form.subtotal = 0
    }
  }
)

/* 重置表单 */
const resetForm = () => {
  form.id = null
  form.content = ''
  form.quantity = null
  form.price = null
  form.subtotal = 0
  form.material = ''
  form.size = null
  form.handler = ''
  form.remark = ''
  form.image = ''
}

/* 重排序号 */
const resetIndex = () => {
  list.value.forEach((item, index) => {
    item.id = index + 1
  })
}

/* 添加数据 */
const addItem = async() => {
  if (
  !form.content ||
  form.quantity === null ||
  form.price === null
) {
    alert('内容、数量、价格为必填项')
    return
  }
const newItem = {
  ...form,
  id: list.value.length + 1,
  subtotal: form.quantity * form.price
}

  list.value.push(newItem)
  await window.api.saveExcel(list.value)
  resetForm()
}

/* 查询*/
const keyword = ref('')

const filteredList = computed(() => {
  if (!keyword.value) return list.value
  return list.value.filter(item =>
    item.content.includes(keyword.value)
  )
})

/* 删除 */
const deleteItem = async(row) => {
list.value = list.value.filter(item => item.id !== row.id)
resetIndex()
await window.api.saveExcel(list.value)
}
/* 修改 */
const editingIndex = ref(null)
const editItem = (row, index) => {
  Object.assign(form, row)
  editingIndex.value = index
}
/* 合计 */
const totalSum = computed(() => {
  return list.value.reduce((sum, item) => {
    return sum + Number(item.subtotal || 0)
  }, 0)
})
</script>