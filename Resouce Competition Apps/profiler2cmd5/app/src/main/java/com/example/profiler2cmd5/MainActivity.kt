package com.example.profiler2cmd5

import android.content.Context
import android.os.Bundle
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
import com.example.profiler2cmd5.ui.theme.Profiler2cmd5Theme
import java.io.RandomAccessFile
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.time.Instant
import java.util.concurrent.Executors
import java.util.concurrent.ThreadFactory
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicLong
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

class MemTasker { // Memory Contention
    private val taskCount = AtomicLong(0)
    private val length = 1_00
    private val dataArray = ArrayList<Long>()
    private var index = 0

    fun executeTask() {
        while (true) {
            dataArray.clear()
            for (i in 0L until length) {
                dataArray.add(i)
            }
            dataArray[index] = dataArray[length - index - 1] + 1 // visit the d[i] and d[n - i - 1]
            index = (index + 1) % length
            taskCount.incrementAndGet()
        }
    }

    fun getTaskCount(): Long = taskCount.get()
    fun getAndResetTaskCount(): Long = taskCount.getAndSet(0)
}

class DiskTasker(context: Context, id: Int) { // Disk I/O Contention
    private val taskCount = AtomicLong(0L)
    private var filePath: Path
    private val dataSize = 1 * 1024 // 4KB
    private val random = Random(Instant.now().toEpochMilli())

    init {
        // Modify the filePath initialization
        filePath = Paths.get(context.filesDir.path, "disk_tasker_data$id.bin")

        prepareFile()
    }

    private fun prepareFile() {
        if (!Files.exists(filePath)) {
            Files.createFile(filePath)
        }
        // Ensure the file is at least 4KB
        RandomAccessFile(filePath.toFile(), "rw").use { raf ->
            raf.setLength(dataSize.toLong())
        }
    }

    fun executeTask() {
        // Prepare a buffer with random data
        val writeBuffer = ByteArray(dataSize)
        random.nextBytes(writeBuffer)

        val readBuffer = ByteArray(dataSize)

        RandomAccessFile(filePath.toFile(), "rw").use { raf ->
            while (true) {

                // write the data to 0 position
                raf.seek(0)
                raf.write(writeBuffer)

                // Read from the 0 position
                raf.seek(0)
                raf.readFully(readBuffer)

                // Flush changes to disk
                raf.fd.sync()

                taskCount.incrementAndGet()
            }
        }
    }

    fun getTaskCount(): Long = taskCount.get()
    fun getAndResetTaskCount(): Long = taskCount.getAndSet(0)
}

class MainActivity : ComponentActivity() {

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

    private val nCpu = 6
    private val nMem = 2
    private val nDisk = 2

    private val cpuTaskers = List(nCpu) { CpuTasker() }
    private val memTaskers = List(nMem) { MemTasker() }

    private lateinit var diskTaskers: List<DiskTasker>

    private val executor = Executors.newFixedThreadPool(nCpu + nMem + nDisk, normalPriorityThreadFactory)
    private val scheduledExecutor = Executors.newSingleThreadScheduledExecutor(normalPriorityThreadFactory)

    private val infoListState = mutableStateListOf<Long>().apply {
        addAll(List(nCpu + nMem + nDisk) { 0L })
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        diskTaskers = List(nDisk) {
            DiskTasker(this, it)
        }

        FileManager.init(this)

        setContent {
            InfoListScreen(infoListState)
        }

        // put the tasker into executor
        cpuTaskers.forEach { tasker ->
            executor.submit {
                tasker.executeTask()
            }
        }
        memTaskers.forEach { tasker ->
            executor.submit {
                tasker.executeTask()
            }
        }
        diskTaskers.forEach { tasker ->
            executor.submit {
                tasker.executeTask()
            }
        }

        val dt = 10L // each dt ms record the job finish num of each tasker
        var sumt = 0L
        scheduledExecutor.scheduleWithFixedDelay({
            sumt += 10L
            if (sumt % 3000 == 0L) { // period = 3s
                val tempInfoList = MutableList(0) { _ -> 0L }
                cpuTaskers.forEach { tempInfoList.add(it.getTaskCount()) }
                memTaskers.forEach { tempInfoList.add(it.getTaskCount()) }
                diskTaskers.forEach { tempInfoList.add(it.getTaskCount()) }
                infoListState.clear()
                infoListState.addAll(tempInfoList)
            }
            val cpu_num = cpuTaskers.sumOf { it.getAndResetTaskCount() }
            val mem_num = memTaskers.sumOf { it.getAndResetTaskCount() }
            val disk_num = diskTaskers.sumOf { it.getAndResetTaskCount() }
            writeToFileSync(cpu_num, mem_num, disk_num)
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