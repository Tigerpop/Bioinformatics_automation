# 设置编码为 UTF-8
options(encoding = "UTF-8")

#  load the package
library(panelcn.mops)
data(panelcn.mops)

# Rscript my_script.R arg1_value arg2_value
# args <- commandArgs(trailingOnly = TRUE)
# arg1 <- args[1]
# arg2 <- args[2]
# my_function(arg1, arg2)
args <- commandArgs(trailingOnly = TRUE)
sample <- args[1]
sample_path <- args[2]
generate_location <- args[3]
bed_key <- args[4] 
print(sample)
print(bed_key)

BC17T <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/BC17/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW000518-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001177-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001194-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001198-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001204-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001203-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001207-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17T/2023WSSW001199-T.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam8, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
                                   )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
BC17B <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/BC17/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17B/2022WSSW005351-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17B/2023WSSW001202-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17B/2022WSSW005739-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BC17B/2023WSSW000522-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}

Q120T <- function(sample,bed) {
  # 获取计数窗
  bed <- bed# "/refhub/hg19/target/Q120/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW001396-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW001289-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW000728-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW001743-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2022WSSW000596-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW000798-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW001792-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120T/2023WSSW001605-T.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam8, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
Q120B <- function(sample,bed) {
  # 获取计数窗
  bed <- bed# "/refhub/hg19/target/Q120/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001375-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001049-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001052-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001054-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001302-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW000727-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW001280-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/Q120B/2023WSSW000636-T.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam8, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
NBC650 <- function(sample) {
  # 获取计数窗
  bed <- "/refhub/hg19/target/NBC650/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004654-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW005125-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004656-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2021WSSW010388-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004677-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004116-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW005590-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/NBC650/2022WSSW004157-T.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam8, read.width = 150)
 # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}

BCP650 <- function(sample) {
  # 获取计数窗
  bed <- "/refhub/hg19/target/BCP650/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2022WSSW000306-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000103-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000052-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000064-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000062-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000659-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2022WSSW005609-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/BCP650/2023WSSW000057-T.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam8, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}

SD160T <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW000844-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001247-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001266-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001264-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001539-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001540-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160T/2023WSSW001744-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
SD160B <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW001589-T.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW000956-T.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW000642-T.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW000641-T.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2022WSSW005623-T.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW000955-T.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SD160B/2023WSSW000731-T.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
SLC17T <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-QNH1182-17T-1G0531.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-ZCY1172-17T-1G0531.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-SGC1096-17T-1G0525.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-ZZY1083-17T-1G0525.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-TYX0746-17T-1G0506.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-WLE1035-17T-1G0524.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/BCX-WZL1059-17T-1G0523.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17T/RC-CJ1067-17T-1G0524.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
SLC17B <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/BCX-LDR0807-17B-2G0508.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/RC-SYJ0947-17B-2G0517.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/BCX-LSQ1134-17B-2G0527.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/RC-JQH1161-17B-2G0530.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/RC-LQB1144-17B-2G0529.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/BCX-WWN1060-17B-2G0523.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/WC-SZH1088-17B-2G0525.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC17B/BCX-PLL1087-17B-2G0525.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
SLC80T <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/BCX-YWG1117-80T-1G0526.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/WL-DTM1082-80T-1G0525.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/BCX-YLD1076-80T-1G0524.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/BCX-XQ1094-80T-1G0525.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/BCX-MWH1064-80T-1G0524.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/RC-HDZ1066-80T-1G0524.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/WL-ZSS1062-80T-1G0524.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80T/BCX-XGL1075-80T-1G0524.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}
SLC80B <- function(sample,bed) {
  # 获取计数窗
  bed <- bed # "/refhub/hg19/target/SD160/panelcn.bed"
  countWindows <- getWindows(bed)
  # 获取read counts
  testbam <- sprintf("/home/chenyushao/py_streaming_generate/%s/%s.bwa_mem.bam", sample,sample)
  cat("testbam is :", testbam, "\n")
  # testbam <- "/home/chenyushao/py_streaming_generate/2022WSSW004338-T/2022WSSW004338-T.bwa_mem.bam"
  test <- countBamListInGRanges(countWindows = countWindows,bam.files = testbam, read.width = 150)
  # 可以和decon公用一套对照。
  controlbam1 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/RSD-SHX0752-80B-2G0505.bwa_mem.bam"
  control1 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam1, read.width = 150)
  controlbam2 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/BCX-LCY0850-80B-2G0510.bwa_mem.bam"
  control2 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam2, read.width = 150)
  controlbam3 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/RC-YLQ0836-80B-2G0510.bwa_mem.bam"
  control3 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam3, read.width = 150)
  controlbam4 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/BCD-ZBP0926-80B-2G0514.bwa_mem.bam"
  control4 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam4, read.width = 150)
  controlbam5 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/BCD-LJS1050-80B-2G0522.bwa_mem.bam"
  control5 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam5, read.width = 150)
  controlbam6 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/BCD-WSM1004-80B-2G0519.bwa_mem.bam"
  control6 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam6, read.width = 150)
  controlbam7 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/RC-XGF1143-80B-2G0529.bwa_mem.bam"
  control7 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  controlbam8 <- "/refhub/hg19/toolbox_and_RefFile/Decon_ref_bam_file_txt/SLC80B/BCX-MWH1063-80B-2G0524.bwa_mem.bam"
  control8 <- countBamListInGRanges(countWindows = countWindows,bam.files = controlbam7, read.width = 150)
  # 运行算法
  XandCB <- test
  elementMetadata(XandCB) <- cbind(elementMetadata(XandCB),
                                   elementMetadata(control1),
                                   elementMetadata(control2),
                                   elementMetadata(control3),
                                   elementMetadata(control4),
                                   elementMetadata(control5),
                                   elementMetadata(control6),
                                   elementMetadata(control7),
                                   elementMetadata(control8)
  )
  resultlist <- runPanelcnMops(XandCB,
                               testiv = 1:ncol(elementMetadata(test)),
                               countWindows = countWindows)
  # 结果可视化
  sampleNames <- colnames(elementMetadata(test))
  resulttable <- createResultTable(resultlist = resultlist, XandCB = XandCB,
                                   countWindows = countWindows,
                                   selectedGenes = NULL,
                                   sampleNames = sampleNames)
  write.table(resulttable, "./panelcn_output.txt", sep="\t", row.names=FALSE)
}

# 
tmp_dir <- paste(generate_location, sample_path, "panelcn_generate", sep="/")
if (!dir.exists(tmp_dir)) {
  dir.create(tmp_dir)
}
setwd(tmp_dir)
if ( bed_key == "BC17T" ) {
  BC17T(sample,bed="/refhub/hg19/target/BC17T/panelcn.bed") 
} else if ( bed_key == "BC17B" ) {
  BC17B(sample,bed="/refhub/hg19/target/BC17B/panelcn.bed") 
} else if ( bed_key == "Q120T" | bed_key == "Q80T" | bed_key == "Q110T") {
  Q120T(sample,bed="/refhub/hg19/target/Q120T/panelcn.bed")
} else if ( bed_key == "Q120B" | bed_key == "Q80B" | bed_key == "Q110B") {
  Q120B(sample,bed="/refhub/hg19/target/Q120B/panelcn.bed")
} else if ( bed_key == "NBC650") {
  NBC650(sample)
} else if ( bed_key == "BCP650") {
  BCP650(sample)
} else if ( bed_key == "SD160T") {
  SD160T(sample,bed="/refhub/hg19/target/SD160T/panelcn.bed")
} else if ( bed_key == "SD160B") {
  SD160B(sample,bed="/refhub/hg19/target/SD160B/panelcn.bed")
} else if ( bed_key == "SLC17T") {
  SLC17T(sample,bed="/refhub/hg19/target/SLC17T/panelcn.bed")
} else if ( bed_key == "SLC17B") {
  SLC17B(sample,bed="/refhub/hg19/target/SLC17B/panelcn.bed")
} else if ( bed_key == "SLC80T") {
  SLC80T(sample,bed="/refhub/hg19/target/SLC80T/panelcn.bed")
} else if ( bed_key == "SLC80B") {
  SLC80B(sample,bed="/refhub/hg19/target/SLC80B/panelcn.bed")
} else {
  print('panel is not exitst.')
}

