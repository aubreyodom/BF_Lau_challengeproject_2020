all_files

temp <- sapply(strsplit(unlist(strsplit(all_files, ".csv")), "CSV_files/"), function(x) x[[2]])
out <- dplyr::tibble(Filenames = temp, Ranking = NA)
View(out)
write.csv(out, "Rankings_template.csv")
