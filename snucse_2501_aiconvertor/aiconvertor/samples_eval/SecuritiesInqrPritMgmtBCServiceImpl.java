
package am.im.securitiesinqrpritmgmt.service.impl;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import am.im.securitiesinqrpritmgmt.service.SecuritiesInqrPritMgmtBCService;
import custom.cmmn.exception.CgAppUserException;
import custom.cmmn.util.MapDataUtil;
import custom.cmmn.util.UserHeaderUtil;
import com.inswave.elfw.exception.ElException;
import com.inswave.ext.cg.util.CodeUtil;


@Service("securitiesInqrPritMgmtBCServiceImpl")
public class SecuritiesInqrPritMgmtBCServiceImpl implements SecuritiesInqrPritMgmtBCService {

    
    
    public ArrayList<Map> selectInterestRtrvDuda(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0015(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0014(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsBalance(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0005(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectDepositsWithdrawal(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0004(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectGnrzReport(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0013(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectCdSalePsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0012(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectBondsSalePsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0011(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectOperatingFundsPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0010(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectFundsExecution(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0009(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectExpirationPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0008(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectMmtLedger(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        String trnsDateFrom = null;
        String trnsDateTo = null;
        try {
            
            
            trnsDateFrom = MapDataUtil.getString(pDoc, "TRNS_DATE_FROM");
            trnsDateTo = MapDataUtil.getString(pDoc, "TRNS_DATE_TO");
            MapDataUtil.setString(pDoc, "TRNS_DATE_FROM1", trnsDateFrom);
            MapDataUtil.setString(pDoc, "TRNS_DATE_TO1", trnsDateTo);
            MapDataUtil.setString(pDoc, "TRNS_DATE_FROM2", trnsDateFrom);
            MapDataUtil.setString(pDoc, "TRNS_DATE_TO2", trnsDateTo);
            MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD1", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));
            MapDataUtil.setString(pDoc, "ESTB_BANK_TRNS_BRCD2", MapDataUtil.getString(pDoc, "ESTB_BANK_TRNS_BRCD"));
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0006(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectSecuritiesLedger(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0002(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectKsdDpstCdBondsPsst(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0001(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public Map selectSecuritiesStrcPrdtInfo(Map pDoc) throws ElException {
        Map result = null;
        Map bizInput = new HashMap();
        ;
        ArrayList<Map> bizOutput = null;
        String invtAvbl = "";
        Long frcrInvtAvbl = 0l;
        String spotEcrt = "";
        Double ecrtUnitVl = 0.0d;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0016(pDoc);
            
            bizOutput = comCgAmImSecuritiesmgmtImzscinvtdtlsDaoDAO.im_zsc_invt_dtls_so0003(pDoc);
            
            
            MapDataUtil.setVector(bizInput, "VECTOR_BALN", bizOutput);
            
            
            
            MapDataUtil.setString(bizInput, "CALC_STDA", MapDataUtil.getString(result, "PUR_DATE"));
            
            MapDataUtil.setString(bizInput, "CALC_ENDA", MapDataUtil.getString(pDoc, "BSDA"));
            
            
            MapDataUtil.setString(bizInput, "ENDA_PREV_FLAG", "Y");
            
            bizOutput = null;
            invtAvbl = MapDataUtil.getString(bizOutput, "INVT_AVBL");
            spotEcrt = MapDataUtil.getString(result, "SPOT_ECRT");
            ecrtUnitVl = MapDataUtil.getDouble(result, "ECRT_UNIT_VL");
            
            
            MapDataUtil.setString(result, "INVT_AVBL", invtAvbl);
            if (!spotEcrt.isEmpty()) {
                
                frcrInvtAvbl = Math.round(Double.parseDouble(invtAvbl) / Double.parseDouble(spotEcrt) * ecrtUnitVl);
                
                MapDataUtil.setString(result, "FRCR_INVT_AVBL", String.valueOf(frcrInvtAvbl));
            }
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectSecuritiesStrcPrdtTrns(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0017(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<Map> selectInvtReturnRate(Map pDoc) throws ElException {
        ArrayList<Map> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0018(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public Map selectVldtDcntCondIntsPaynCond(Map pDoc) throws ElException {
        Map result = null;
        ArrayList<Map> intsPaynCondCdDoc = null;
        ArrayList<Map> vldtDcntCondCdDoc = null;
        try {
            result = new HashMap();
            
            
            intsPaynCondCdDoc = comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_so0001(pDoc);
            
            vldtDcntCondCdDoc = comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_so0001(pDoc);
            
            MapDataUtil.setList(result, "INTS_PAYN_COND_CD_LIST", intsPaynCondCdDoc);
            
            MapDataUtil.setList(result, "VLDT_DCNT_COND_CD_LIST", vldtDcntCondCdDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public Map saveVldtDcntCondIntsPaynCond(Map pDoc) throws ElException {
        Map result = null;
        Map intsPaynCondCdDoc = null;
        Map vldtDcntCondCdDoc = null;
        Map listInts = null;
        Map listVldt = null;
        Map resultInts = null;
        Map resultVldt = null;
        String errCd = "";
        String errMsg = "";
        try {
            
            
            intsPaynCondCdDoc = /* 주석처리(as-is) XMLUtil.toXML(XMLUtil.getVector(pDoc, "INTS_PAYN_COND_CD_LIST"))*/;
            ArrayList aryListInts = /* 수동가이드 예정 (as-is) XMLUtil.toArrayList(intsPaynCondCdDoc)*/;
            Iterator<Map> itrInts = aryListInts.iterator();
            
            while (itrInts.hasNext()) {
                listInts = itrInts.next();
                
                MapDataUtil.setString(listInts, "LAST_CHNR_ID", (String) UserHeaderUtil.getInstance().getEmpno());
                
                MapDataUtil.setString(listInts, "LAST_CHNG_DTTM", (String) UserHeaderUtil.getInstance().getTimestamp());
                
                if (("3").equals(MapDataUtil.getAttribute(listInts, "status"))) {
                    
                    resultInts = comCgAmImSecuritiesinqrpritmgmtImzscstrcintscondDaoDAO.im_zsc_strc_ints_cond_so0002(listInts);
                    if (MapDataUtil.getInt(resultInts, "CNT") > 0) {
                        errCd = "E00000";
                        errMsg = "현재 사용하고 있는 조건입니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_do0001(listInts);
                } else if (("2").equals(MapDataUtil.getAttribute(listInts, "status"))) {
                    
                    resultInts = comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_so0003(listInts);
                    if (MapDataUtil.getInt(resultInts, "CNT") > 0) {
                        errCd = "E00000";
                        errMsg = "동일한 조건이 있습니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_io0001(listInts);
                } else if (("1").equals(MapDataUtil.getAttribute(listInts, "status"))) {
                    
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_uo0001(listInts);
                }
            }
            
            vldtDcntCondCdDoc = /* 주석처리(as-is) XMLUtil.toXML(XMLUtil.getVector(pDoc, "VLDT_DCNT_COND_CD_LIST"))*/;
            ArrayList aryListVldt = /* 수동가이드 예정 (as-is) XMLUtil.toArrayList(vldtDcntCondCdDoc)*/;
            Iterator<Map> itrVldt = aryListVldt.iterator();
            while (itrVldt.hasNext()) {
                listVldt = itrVldt.next();
                
                MapDataUtil.setString(listVldt, "LAST_CHNR_ID", (String) UserHeaderUtil.getInstance().getEmpno());
                
                MapDataUtil.setString(listVldt, "LAST_CHNG_DTTM", (String) UserHeaderUtil.getInstance().getTimestamp());
                
                if (("3").equals(MapDataUtil.getAttribute(listVldt, "status"))) {
                    
                    resultVldt = comCgAmImSecuritiesinqrpritmgmtImzscstrcvldtdcntcondDaoDAO.im_zsc_strc_vldt_dcnt_cond_so0001(listVldt);
                    if (MapDataUtil.getInt(resultVldt, "CNT") > 0) {
                        errCd = "E00000";
                        errMsg = "현재 사용하고 있는 조건입니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_do0001(listVldt);
                } else if (("2").equals(MapDataUtil.getAttribute(listVldt, "status"))) {
                    
                    resultVldt = comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_so0003(listVldt);
                    if (MapDataUtil.getInt(resultVldt, "CNT") > 0) {
                        errCd = "E00000";
                        errMsg = "동일한 조건이 있습니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_io0001(listVldt);
                } else if (("1").equals(MapDataUtil.getAttribute(listVldt, "status"))) {
                    
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_uo0001(listVldt);
                }
            }
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

}