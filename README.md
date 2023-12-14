# py_qml_lanton_ant

蘭頓螞蟻（英語：Langton's ant）是細胞自動機的例子。
它由克里斯托夫·蘭頓在1986年提出，它由黑白格子和一隻「螞蟻」構成[1]，是一個二維圖靈機。
蘭頓螞蟻擁有非常簡單的邏輯和複雜的表現。在2000年蘭頓螞蟻的圖靈完備性被證明。

在平面上的正方形格被填上黑色或白色。在其中一格正方形有一隻「螞蟻」。它的頭部朝向上下左右其中一方。

    * 若螞蟻在白格，右轉90度，將該格改為黑格，向前移一步；
    * 若螞蟻在黑格，左轉90度，將該格改為白格，向前移一步。

以上引用自維基百科
https://zh.wikipedia.org/zh-tw/%E5%85%B0%E9%A1%BF%E8%9A%82%E8%9A%81

專案特點：

    * 非常簡潔：
        。只有 python 跟 QML 檔案，直接執行 main.py 即可
        。資料庫使用 sqlite3, 自動產生資料檔，自動創建資料表
    * 可在程式碼修改運算矩陣大小，格子大小。
    * UI界面
        。可按百分比隨機產生有顏色的格子
        。可將地圖布局存檔/載入/刪除
        。滑鼠點擊編輯地圖
        。開始/暫停
        。單部執行
        。加速/減速運行速度
        。螞蟻移動時有動畫效果

![img.png](img.png)

目前測試通過的平台

    * Mac OSX 14 + Python 3.11.6 

    * Windows 11 + Python 3.11.6
