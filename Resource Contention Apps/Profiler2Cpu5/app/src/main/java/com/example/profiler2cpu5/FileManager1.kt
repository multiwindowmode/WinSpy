package com.example.profiler2cpu5

import android.content.Context
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object FileManager1 {
    private var bufferedStream_bged: BufferedOutputStream? = null
    private var bufferedStream_rec: BufferedOutputStream? = null

    fun init(context: Context) {
        val file_bged = File(context.filesDir, "begin_end.txt")
        bufferedStream_bged = BufferedOutputStream(FileOutputStream(file_bged, true))
        val file_rec = File(context.filesDir, "hhz.txt")
        bufferedStream_rec = BufferedOutputStream(FileOutputStream(file_rec, true))
    }

    fun writeMessage_bged(message: String) {
        try {
            bufferedStream_bged?.let {
                it.write(message.toByteArray())
                it.flush()
            }
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    fun writeMessage_rec(message: String) {
        try {
            bufferedStream_rec?.let {
                it.write(message.toByteArray())
                it.flush()
            }
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    fun close() {
        try {
            bufferedStream_bged?.flush()
            bufferedStream_bged?.close()
            bufferedStream_rec?.flush()
            bufferedStream_rec?.close()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }
}

object FileManager {
    private var bufferedStream: BufferedOutputStream? = null

    fun init(context: Context) {
//        val file = File(context.getExternalFilesDir(null), "ext_cpu_mem_disk_record.txt")
        val file = File(context.filesDir, "ext_cpu_mem_disk_record.txt")
        bufferedStream = BufferedOutputStream(FileOutputStream(file, true))
    }

//    fun init(context: Context) {
//        // Use internal storage
//        val file = File(context.filesDir, "ext_cpu_mem_disk_record.txt")
//        bufferedStream = BufferedOutputStream(FileOutputStream(file, true))
//    }

    fun write(message: String) {
        try {
            bufferedStream?.write(message.toByteArray())
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    fun flush() {
        bufferedStream!!.flush()
    }

    fun close() {
        try {
            bufferedStream?.flush()
            bufferedStream?.close()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }
}

object Timer1 {
    fun gett(): String {
        return SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.getDefault()).format(Date())
    }
}