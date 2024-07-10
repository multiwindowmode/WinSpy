package com.example.tappingimu10_phone

import android.util.Log
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun checkCurrentThread() {
    val threadName = Thread.currentThread().name
    Log.d("tttt", "This function is running on thread: $threadName")
}

val formatter: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS")

val formatter2: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyy_MM_dd_HH_mm_ss_SSS")

fun getCurrentDateTimeFormatted(): String {
    return formatter.format(LocalDateTime.now())
}

val fileTimeName: String = formatter2.format(LocalDateTime.now())