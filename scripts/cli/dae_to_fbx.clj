#!/usr/bin/env bb
(require '[babashka.fs :as fs])
(require '[babashka.process :refer [shell]])
(require '[clojure.pprint :refer [pprint]])

;; TODO Extract these out into CLI usage
(def settings {:in-path "W:\\Blender\\work\\__OBJECTS"
               :glob "**.dae"
               :tool-path "C:\\Program Files\\Autodesk\\FBX\\FBX Converter\\2013.3\\bin\\FbxConverter.exe"})

;; ---

(defn dae->fbx-path
  "Just change whatever extension the file has into .fbx"
  [path]
  (fs/path (str (fs/strip-ext path) ".fbx")))

(defn collect-convertable
  "Gather a list of DAE files that need to be converted to FBX."
  [file-list]
  ;; first find files that need converting
  (loop [xs (seq file-list)
         result []]
    (if xs
      (let [x (first xs)
            fbx-filename (dae->fbx-path x)
            fbx-exists? (fs/exists? fbx-filename)]
        (recur
         (next xs)
         (if fbx-exists? result (conj result {:from x :to fbx-filename}))))

      ;; if we don't have any items on the list, bail out
      result)))

;; ---

(defn main
  []
  (let [files (fs/glob (:in-path settings) (:glob settings))
        convertable-files (collect-convertable files)
        conv-count (count convertable-files)
        bin (:tool-path settings)]
    (println (str "Found " conv-count " files to convert."))

    (loop [remaining (seq convertable-files)
           converted []]
      (if remaining
        (let [t (first remaining)
              f1 (:from t)
              f2 (:to t)]
          ;; convert dae->fbx
          (try
            (println (str f1))
            (println (str " -> " f2))
            (shell bin f1 f2)
            (catch Exception e (println e)))


          (recur
           (next remaining)
           (conj converted f2)))
        converted))))

;; ---

(main)
