#!/usr/bin/env python

import utils
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import collections


def features_from_track(track, properties):
    for seg in track.segments:
        yield features_from_segment(seg, properties)


def features_from_segment(segment, properties):
    feature = []
    for prop in properties:
        item = segment.get(prop, None)
        if isinstance(item, collections.Iterable):
            feature += list(item)
        elif item is not None:
            feature.append(item)
    return feature


def find_center_segments(X, centers):
    indicies = []
    for center in centers:
        indicies.append(np.power(np.sum(X - center, axis=1),2).argmin())
    return indicies

if __name__ == "__main__":
    features_list = ("pitches", "timbre")
    chad = utils.track_with_file("data/Chad_VanGaalen_Willow_Tree.wav", track_id=u'TRP8KVE11BC6E02570') #Chad VanGaalen - Willow Tree
    features = np.asarray(list(features_from_track(chad, features_list)))

    reducer = PCA(n_components=0.7)
    features_reduced = reducer.fit_transform(features)
    print "Keeping %d/%d indicies"%(features_reduced.shape[1], features.shape[1])
    
    cluster = KMeans(k=50, n_init=25, max_iter=500).fit(features_reduced)
    center_idx = find_center_segments(features_reduced, cluster.cluster_centers_)

    print "Playing"
    for seg in chad.segments:
        idx = center_idx[cluster.predict(reducer.transform( features_from_segment(seg, features_list)  ))[0]]
        utils.play_segment(chad.segments[idx])

