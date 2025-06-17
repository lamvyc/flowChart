<template>
  <div>
    <!-- 操作栏 -->
    <a-space style="margin-bottom: 16px">
      <a-button type="primary" @click="saveChart">保存流程图</a-button>
    </a-space>

    <div class="flow-chart" ref="container" />
  </div>

  <!-- 配置表单抽屉 -->
  <a-drawer
    v-model:visible="drawerVisible"
    :title="drawerTitle"
    width="400"
    destroyOnClose
  >
    <a-form
      :model="formState"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      @submit.prevent="handleSubmit"
    >
      <a-form-item
        label="负责人"
        name="owner"
        :rules="[{ required: true, message: '请输入负责人' }]"
      >
        <a-input v-model:value="formState.owner" placeholder="请输入负责人" />
      </a-form-item>

      <a-form-item label="截止时间" name="deadline">
        <a-date-picker v-model:value="formState.deadline" style="width: 100%" />
      </a-form-item>

      <a-form-item :wrapper-col="{ span: 24, offset: 6 }">
        <a-button type="primary" html-type="submit">提交</a-button>
      </a-form-item>
    </a-form>
  </a-drawer>
</template>

<script setup lang="ts">
// @ts-nocheck
import { onMounted, ref, reactive, computed } from 'vue';
import G6, { Graph as G6Graph, IG6GraphEvent, Item } from '@antv/g6';
import { message } from 'ant-design-vue';
import {
  createChart,
  getCharts,
  getChart,
  Chart,
  ChartMeta,
} from '../api/charts';

interface NodeData {
  id: string;
  label: string;
}

interface FormState {
  owner: string;
  deadline: string | undefined;
}

const container = ref<HTMLDivElement | null>(null);
const graph = ref<G6Graph | null>(null);
const drawerVisible = ref(false);
const currentNode = ref<NodeData | null>(null);

const formState = reactive<FormState>({
  owner: '',
  deadline: undefined,
});

const drawerTitle = computed(() => {
  return currentNode.value ? `${currentNode.value.label} 节点配置` : '';
});

function initGraph(el: HTMLDivElement) {
  const data = {
    nodes: [
      { id: 'label', label: '标注', x: 100, y: 100 },
      { id: 'review', label: '审核', x: 300, y: 100 },
      { id: 'accept', label: '验收', x: 500, y: 100 },
    ],
    edges: [
      { source: 'label', target: 'review' },
      { source: 'review', target: 'accept' },
    ],
  };

  graph.value = new G6.Graph({
    container: el,
    width: el.clientWidth || 600,
    height: 300,
    modes: { default: ['drag-node'] },
    defaultNode: {
      size: 60,
      style: {
        fill: '#E6F7FF',
        stroke: '#1890FF',
      },
      labelCfg: {
        style: {
          fill: '#1890FF',
          fontSize: 14,
        },
      },
    },
    defaultEdge: {
      style: {
        stroke: '#A3B1BF',
      },
      endArrow: {
        path: G6.Arrow.triangle(10, 12, 8),
        fill: '#A3B1BF',
      },
    },
  });

  graph.value.data(data);
  graph.value.render();

  graph.value.on('node:click', (evt: IG6GraphEvent) => {
    const item = evt.item as Item;
    const model = item.getModel() as NodeData;
    currentNode.value = model;

    // reset form for each node
    formState.owner = '';
    formState.deadline = undefined;

    drawerVisible.value = true;
  });
}

onMounted(() => {
  if (container.value) {
    initGraph(container.value);

    // 尝试加载后端最新一条流程图
    getCharts()
      .then((list: ChartMeta[]) => {
        if (list.length === 0) return;
        // 取最新 (id 最大) 的流程图
        return getChart(list[0].id);
      })
      .then((chart?: Chart) => {
        if (chart && graph.value) {
          graph.value.clear();
          graph.value.data(chart.data);
          graph.value.render();
          message.success(`已加载后端流程图：${chart.name}`);
        }
      })
      .catch(() => {
        /* ignore */
      });
  }
});

function handleSubmit() {
  drawerVisible.value = false;
  message.success(`${drawerTitle.value} 已提交！`);
  // 这里可以发送 API 请求或 emit 事件将表单数据交给父组件
  console.log('提交数据', {
    nodeId: currentNode.value?.id,
    ...formState,
  });
}

/**
 * 将当前画布数据保存到后端
 */
function saveChart() {
  if (!graph.value) return;
  const data = graph.value.save();
  createChart({ name: `流程图_${Date.now()}`, data })
    .then(() => {
      message.success('保存成功！');
    })
    .catch(() => {
      message.error('保存失败');
    });
}
</script>

<style scoped>
.flow-chart {
  width: 100%;
  height: 300px;
  border: 1px solid #dcdcdc;
}
</style> 