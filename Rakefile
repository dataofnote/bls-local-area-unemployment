require 'pathname'
DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR. / 'corral'
SCRIPTS_DIR = WRANGLE_DIR / 'scripts'
DIRS = {
    :fetched => CORRAL_DIR / ('fetched'),
    :compiled => CORRAL_DIR / ('compiled'),
    :published => DATA_DIR,
}

P_FILES = Hash[{
    fips: 'fips.csv',
    counties_states_unadjusted: 'bls-local-area-unemployment-counties-states-unadjusted.csv',
    counties_states_unadjusted_averages: 'bls-local-area-unemployment-counties-states-unadjusted-averages.csv',
    states_seasonal: 'bls-local-area-unemployment-states-seasonally-adjusted.csv',
    states_seasonal_averages: 'bls-local-area-unemployment-states-seasonally-adjusted-averages.csv',

}.map{|k, v| [k, DATA_DIR / v ] }]

I_FILES = Hash[{
    counties_states_unadjusted: 'counties-states-unadjusted.csv',
    counties_states_unadjusted_averages: 'counties-states-unadjusted-averages.csv',
    states_seasonal: 'states-seasonally-adjusted.csv',
    states_seasonal_averages: 'states-seasonally-adjusted-averages.csv',
}.map{|k, v| [k, DIRS[:compiled] / v ] }]


desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end

namespace :publish do
    P_FILES.each_pair do |key, pname|
        if I_FILES[key]
            srcname = I_FILES[key]
            desc "Publish #{key}"
            file pname => srcname do
                sh "cp #{srcname} #{pname}"
            end
        end
    end
end



desc 'counties and states average annual unemployment, unadjusted'
file I_FILES[:counties_states_unadjusted_averages] => I_FILES[:counties_states_unadjusted] do
    sh [
        "python",
        SCRIPTS_DIR / 'calculate_averages.py',
        I_FILES[:counties_states_unadjusted],
        '>', I_FILES[:counties_states_unadjusted_averages]].join(" ")
end

desc 'counties and states extracted'
file I_FILES[:counties_states_unadjusted] do
    sh [
        "cat", DIRS[:fetched] / 'la.data.64.County',
        DIRS[:fetched] / 'la.data.2.AllStatesU',
        '|', "python",
        SCRIPTS_DIR / 'extract_data.py', '-',
        '>', I_FILES[:counties_states_unadjusted]].join(" ")
end




desc 'states extracted, averaged yearly'
file I_FILES[:states_seasonal_averages] => I_FILES[:states_seasonal] do
    sh [
        "python",
        SCRIPTS_DIR / 'calculate_averages.py',
        I_FILES[:states_seasonal],
        '--seasonal',
        '>', I_FILES[:states_seasonal_averages]].join(" ")
end


desc 'states extracted, adjusted data only'
file I_FILES[:states_seasonal] do
    sh [
        "python",
        SCRIPTS_DIR / 'extract_data.py',
        DIRS[:fetched] / 'la.data.3.AllStatesS',
        '--seasonal',
        '>', I_FILES[:states_seasonal]].join(" ")
end





desc "Fetch FIPS lookups from BLS"
file P_FILES[:fips] do
    sh ["python",
            SCRIPTS_DIR / 'fetch_fips.py',
            '>', P_FILES[:fips]].join(" ")
end




