package com.example.profiler2cpu5

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.profiler2cpu5.FileManager
import com.example.profiler2cpu5.Timer1
import com.example.profiler2cpu5.ui.theme.Profiler2Cpu5Theme
import java.time.Instant
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicLong
import java.util.concurrent.ThreadFactory
import kotlin.math.abs
import kotlin.math.cos
import kotlin.math.exp
import kotlin.math.ln
import kotlin.math.log10
import kotlin.math.sin
import kotlin.math.sqrt
import kotlin.random.Random

class CpuTasker { // Cpu Contention
    private val taskCount = AtomicLong(0L)
    private var ji = Random(Instant.now().toEpochMilli()).nextDouble()

    fun executeTask() {
        while (true) {
            val a = abs(ji) + 10 // > 10
            val b = sqrt(taskCount.toDouble() + a) // > 0
            val c = log10(a) * cos(ln(a)) / b + sin(a + b)
            val d = exp(-1 * (a + cos(b) + c * c))
            ji = d
            taskCount.incrementAndGet() // use AtomicInteger to safely increment
        }
    }

    fun getTaskCount(): Long = taskCount.get()

    fun getAndResetTaskCount(): Long = taskCount.getAndSet(0)
}

class MainActivity : ComponentActivity() {

    private val thread_num = 5
    private val cpuTaskers = List(thread_num) { CpuTasker() }

    private val highPriorityThreadFactory = ThreadFactory { runnable ->
        Thread(runnable).apply {
            priority = Thread.MAX_PRIORITY
        }
    }
    private val normalPriorityThreadFactory = ThreadFactory { runnable ->
        Thread(runnable).apply {
            priority = Thread.NORM_PRIORITY
        }
    }
    private val executor = Executors.newFixedThreadPool(thread_num, normalPriorityThreadFactory)
    private val scheduledExecutor = Executors.newSingleThreadScheduledExecutor(highPriorityThreadFactory)

//    private val executor = Executors.newFixedThreadPool(thread_num)
//    private val scheduledExecutor = Executors.newSingleThreadScheduledExecutor()

    private val infoListState = mutableStateListOf<Long>().apply {
        addAll(List(thread_num) { 0L })
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        FileManager.init(this)

//        for (i in 1..10000000) {
//            FileManager.write("$i\n")
//            FileManager.flush()
//        }

        setContent {
            InfoListScreen(infoListState)
        }

        // put the tasker into executor
        cpuTaskers.forEach { tasker ->
            executor.submit {
                tasker.executeTask()
            }
        }

        val dt = 10L // each dt ms record the job finish num of each tasker
        var sumt = 0L
        scheduledExecutor.scheduleAtFixedRate({
            sumt += 10L
            if (sumt % 3000L == 0L) {
                val tempInfoList = List(thread_num) { i ->
                    cpuTaskers[i].getTaskCount()
                }
                infoListState.clear()
                infoListState.addAll(tempInfoList)
                val sum_counter = tempInfoList.sum()
                infoListState.add(sum_counter)
                Log.i("alive", "alive, $sum_counter")
            }
//
//            if (sumt % 300L == 0L) {
//                val tempInfoList = List(thread_num) { i ->
//                    cpuTaskers[i].getTaskCount()
//                }
//                infoListState.clear()
//                infoListState.addAll(tempInfoList)
//                infoListState.add(tempInfoList.sum())
//            }

            val cpu_num = cpuTaskers.sumOf { it.getAndResetTaskCount() }
            writeToFileSync(cpu_num, 0L, 0L)

        }, 0, dt, TimeUnit.MILLISECONDS)
    }

    private fun writeToFileSync(taskCountCpu: Long, taskCountMem: Long, taskCountDisk: Long) {
        val formattedDateTime = Timer1.gett()

        val data = "$formattedDateTime $taskCountCpu $taskCountMem $taskCountDisk\n"

        FileManager.write(data)
    }

    override fun onDestroy() {
        super.onDestroy()
        FileManager.close()
        executor.shutdown()
        scheduledExecutor.shutdown()
    }

}

@Composable
fun InfoListScreen(infoList: SnapshotStateList<Long>) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Task Counts:")
        infoList.forEachIndexed { index, count ->
            Text("Tasker $index: $count")
        }
    }
}